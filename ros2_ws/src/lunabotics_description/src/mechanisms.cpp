// Kinematic mechanism demonstration. Material handoff is scripted, not DEM.
#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo_ros/node.hpp>
#include <std_msgs/msg/bool.hpp>
#include <std_msgs/msg/float32.hpp>
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
 rclcpp::Subscription<std_msgs::msg::Bool>::SharedPtr exc_sub,dump_sub;
 rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr fill_pub;
 std::atomic<bool> excavate{false},dump{false};
 double exc_time=-100,dump_time=-100,last=0,phase=0,angle=0;
 std::set<std::string> collected, delivered;
 std::mutex mutex;
 public:
 void Load(physics::ModelPtr m,sdf::ElementPtr s) override {
  model=m;node=gazebo_ros::Node::Get(s);
  exc_sub=node->create_subscription<std_msgs::msg::Bool>("/excavator/enable",10,[this](std_msgs::msg::Bool::SharedPtr v){std::lock_guard<std::mutex> l(mutex);excavate=v->data;exc_time=model->GetWorld()->SimTime().Double();});
  dump_sub=node->create_subscription<std_msgs::msg::Bool>("/bucket/dump",10,[this](std_msgs::msg::Bool::SharedPtr v){std::lock_guard<std::mutex> l(mutex);dump=v->data;dump_time=model->GetWorld()->SimTime().Double();});
  fill_pub=node->create_publisher<std_msgs::msg::Float32>("/simulation/bucket_load",10);
  update=event::Events::ConnectWorldUpdateBegin(std::bind(&LunarMechanisms::Tick,this));
 }
 void Tick(){
  std::lock_guard<std::mutex> lock(mutex);
  double now=model->GetWorld()->SimTime().Double(),dt=std::max(0.,std::min(.05,now-last));last=now;
  bool run=excavate && now-exc_time<.5, tip=dump && now-dump_time<.5;
  angle+=std::clamp((tip?1.0:0.)-angle,-dt*.15,dt*.15);
  auto b=model->GetJoint("bucket_joint"),g=model->GetJoint("ramp_joint");
  if(b)b->SetPosition(0,angle);if(g)g->SetPosition(0,tip?-1.55:0.);
  for(auto side:{"left","right"}){auto a=model->GetJoint(std::string("actuator_rod_")+side+"_joint");if(a)a->SetPosition(0,angle*.2);}
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
