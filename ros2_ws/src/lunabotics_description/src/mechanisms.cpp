// Kinematic mechanism demonstration. Material handoff is scripted, not DEM.
#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo_ros/node.hpp>
#include <std_msgs/msg/bool.hpp>
#include <std_msgs/msg/float32.hpp>
#include <std_msgs/msg/float32_multi_array.hpp>
#include <atomic>
#include <algorithm>
#include <cmath>
#include <set>
#include <mutex>
#include <functional>
namespace gazebo {
class LunarMechanisms : public ModelPlugin {
 physics::ModelPtr model;
 gazebo_ros::Node::SharedPtr node;
 event::ConnectionPtr update;
 rclcpp::Subscription<std_msgs::msg::Bool>::SharedPtr exc_sub,dump_sub,deploy_sub,latch_sub,hold_sub;
 rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr fill_pub;
 rclcpp::Publisher<std_msgs::msg::Float32MultiArray>::SharedPtr feedback;
 bool deploy=false,release=false,hold=true,latched=true;
 double deploy_time=-100,latch_time=-100,hold_time=-100,deployment=-.25;
 std::atomic<bool> excavate{false},dump{false};
 double exc_time=-100,dump_time=-100,last=0,phase=0,angle=0;
 std::set<std::string> collected, delivered;
 std::mutex mutex;
 public:
 void Load(physics::ModelPtr m,sdf::ElementPtr s) override {
  model=m;node=gazebo_ros::Node::Get(s);
  exc_sub=node->create_subscription<std_msgs::msg::Bool>("/excavator/enable",10,[this](std_msgs::msg::Bool::SharedPtr v){std::lock_guard<std::mutex> l(mutex);excavate=v->data;exc_time=model->GetWorld()->SimTime().Double();});
  dump_sub=node->create_subscription<std_msgs::msg::Bool>("/bucket/dump",10,[this](std_msgs::msg::Bool::SharedPtr v){std::lock_guard<std::mutex> l(mutex);dump=v->data;dump_time=model->GetWorld()->SimTime().Double();});
  deploy_sub=node->create_subscription<std_msgs::msg::Bool>("/excavator/deploy",10,[this](std_msgs::msg::Bool::SharedPtr v){std::lock_guard<std::mutex> l(mutex);deploy=v->data;deploy_time=model->GetWorld()->SimTime().Double();});
  latch_sub=node->create_subscription<std_msgs::msg::Bool>("/bucket/latch_release",10,[this](std_msgs::msg::Bool::SharedPtr v){std::lock_guard<std::mutex> l(mutex);release=v->data;latch_time=model->GetWorld()->SimTime().Double();});
  hold_sub=node->create_subscription<std_msgs::msg::Bool>("/mechanisms/hold",10,[this](std_msgs::msg::Bool::SharedPtr v){std::lock_guard<std::mutex> l(mutex);hold=v->data;hold_time=model->GetWorld()->SimTime().Double();});
  feedback=node->create_publisher<std_msgs::msg::Float32MultiArray>("/simulation/mechanisms",10);
  fill_pub=node->create_publisher<std_msgs::msg::Float32>("/simulation/bucket_load",10);
  update=event::Events::ConnectWorldUpdateBegin(std::bind(&LunarMechanisms::Tick,this));
 }
 void Tick(){
  std::lock_guard<std::mutex> lock(mutex);
  double now=model->GetWorld()->SimTime().Double(),dt=std::max(0.,std::min(.05,now-last));last=now;
  bool active=!hold && now-hold_time<.5 && now-deploy_time<.5 && now-latch_time<.5 && now-dump_time<.5;
  auto b=model->GetJoint("bucket_joint"),g=model->GetJoint("rear_door_joint");
  if(active && release)latched=false;
  // Passive door closes through gravity; never pull it shut with a door motor.
  if(active && !release && angle<.03 && g && std::abs(g->Position(0))<.04 && std::abs(g->GetVelocity(0))<.1)latched=true;
  if(g){g->SetLowerLimit(0,0);g->SetUpperLimit(0,latched?0.:1.6);}
  bool tip=active && dump && !latched && deployment<-.24;
  if(active){
   angle+=std::clamp((tip?1.0:0.)-angle,-dt*.15,dt*.15);
   if(angle<.03 && latched)deployment+=std::clamp((deploy?0.:-.25)-deployment,-dt*.05,dt*.05);
  }
  if(b)b->SetPosition(0,angle);
  auto lift=model->GetJoint("excavator_deploy_joint");if(lift)lift->SetPosition(0,deployment);
  bool run=active && excavate && now-exc_time<.5 && deployment>-.01 && angle<.03 && latched;
  for(auto side:{"left","right"}){auto a=model->GetJoint(std::string("actuator_rod_")+side+"_joint");if(a)a->SetPosition(0,angle*.2);}
  for(auto side:{"left","right"}){auto a=model->GetJoint(std::string("excavator_rod_")+side+"_joint");if(a)a->SetPosition(0,(deployment+.25)*.6);}
  std_msgs::msg::Float32MultiArray state;
  state.data={static_cast<float>(deployment),static_cast<float>(angle),static_cast<float>(g?g->Position(0):0.),latched?1.f:0.f};feedback->publish(state);
  if(run)phase+=dt*.12;
  auto conv=model->GetLink("conveyor");
  for(int i=0;i<7 && conv;i++){
   auto scoop=model->GetJoint("scoop_"+std::to_string(i)+"_joint");
   if(scoop){double z=.1+std::fmod(phase+i*.145,.95); scoop->SetPosition(0,z-.1);}
  }
  // A near-intake rock is carried visibly up the conveyor, then released above bucket.
  if(conv)for(auto rock:model->GetWorld()->Models()){
   const auto name=rock->GetName(); if(name.rfind("regolith_",0)!=0)continue;
   auto local=conv->WorldPose().Inverse()*rock->WorldPose();
   if(run && collected.count(name)==0 && local.Pos().Z()<.18 && local.Pos().Z()>-.15 && std::abs(local.Pos().Y())<.24 && std::abs(local.Pos().X())<.25)collected.insert(name);
   if(collected.count(name) && !delivered.count(name) && run && local.Pos().Z()<1.04){
    local.Pos().Z()+=dt*.12;local.Pos().X()=.08;
    rock->SetWorldPose(conv->WorldPose()*local);rock->SetLinearVel({0,0,0});
    if(local.Pos().Z()>=1.04){rock->SetWorldPose(model->WorldPose()*ignition::math::Pose3d(.05,0,.45,0,0,0));delivered.insert(name);}
   }
  }
  std_msgs::msg::Float32 f;f.data=delivered.size();fill_pub->publish(f);
 }
};
GZ_REGISTER_MODEL_PLUGIN(LunarMechanisms)
}
