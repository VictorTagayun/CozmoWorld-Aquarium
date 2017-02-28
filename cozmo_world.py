import cozmo
import asyncio
from Common.woc import WOC
from cozmo.util import distance_mm, speed_mmps, degrees
import random

'''
@class CozmoWorld
Let Cozmo interact with objects in a world of his own and watch him enjoy himself
@author - Wizards of Coz
'''

class CozmoWorld(WOC):    
    def __init__(self):
        WOC.__init__(self)
        self.board_length = 250
        self.board_breadth = 200
        self.objects = None
        self.cube_id = [0, 0, 0]
        self.robot = None
        cozmo.connect(self.run)    

    async def take_a_nap(self):
        await self.robot.go_to_object(self.objects[0], distance_mm(150)).wait_for_completed()
        await self.robot.turn_in_place(cozmo.util.Angle(degrees=180)).wait_for_completed()
        await self.robot.drive_straight(distance_mm(-160), speed_mmps(20)).wait_for_completed()
        await self.robot.play_anim_trigger(cozmo.anim.Triggers.GoToSleepGetIn).wait_for_completed()
        sleep_for_seconds = cozmo.util.Timeout(timeout=random.randrange(5,15))
        while sleep_for_seconds.is_timed_out is False:
            await self.robot.play_anim_trigger(cozmo.anim.Triggers.GoToSleepSleeping).wait_for_completed()
        await self.robot.play_anim_trigger(cozmo.anim.Triggers.GoToSleepGetOut).wait_for_completed()
        await self.robot.drive_straight(distance_mm(20), speed_mmps(100)).wait_for_completed()

    async def get_scared(self):
        await self.robot.go_to_object(self.objects[0], distance_mm(200)).wait_for_completed()
        await self.robot.play_anim("anim_reacttocliff_edgeliftup_01").wait_for_completed()
        await self.robot.play_anim("anim_triple_backup").wait_for_completed()
        await self.robot.turn_in_place(cozmo.util.Angle(degrees=180)).wait_for_completed()
        await self.robot.drive_straight(distance_mm(100), speed_mmps(200)).wait_for_completed()

    async def speak_through_megaphone(self):
        await self.robot.go_to_object(self.objects[0], distance_mm(70)).wait_for_completed()
        await self.robot.say_text("Hello", duration_scalar=1, voice_pitch=-1).wait_for_completed()
        self.robot.set_robot_volume(0.2)
        await self.robot.say_text("Hello", duration_scalar=1, voice_pitch=-1).wait_for_completed()
        self.robot.set_robot_volume(1)
        x = random.randrange(3)
        if x == 0:
            await self.robot.say_text("Is, anyone there", duration_scalar=1.2, voice_pitch=-1).wait_for_completed()
            self.robot.set_robot_volume(0.2)
            await self.robot.say_text("Is, anyone there", duration_scalar=1.2, voice_pitch=-1).wait_for_completed()
        elif x == 1:
            await self.robot.say_text("All hail, Cozmo", duration_scalar=1.2, voice_pitch=-1).wait_for_completed()
            self.robot.set_robot_volume(0.2)
            await self.robot.say_text("All hail, Cozmo", duration_scalar=1.2, voice_pitch=-1).wait_for_completed()
        elif x == 2:
            await self.robot.say_text("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", duration_scalar=0.1, voice_pitch=-1).wait_for_completed()
            self.robot.set_robot_volume(0.2)
            await self.robot.say_text("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", duration_scalar=0.1, voice_pitch=-1).wait_for_completed()
        self.robot.set_robot_volume(1)
        await self.robot.say_text("Bye bye", duration_scalar=1.2, voice_pitch=-1).wait_for_completed()
        self.robot.set_robot_volume(0.2)
        await self.robot.say_text("Bye bye", duration_scalar=1.2, voice_pitch=-1).wait_for_completed()
        self.robot.set_robot_volume(1)
        await self.robot.turn_in_place(cozmo.util.Angle(degrees=180)).wait_for_completed()

    async def interact_with_treasure(self):
        await self.robot.go_to_object(self.objects[0], distance_mm(100)).wait_for_completed()
        await self.robot.play_anim("anim_reacttoblock_admirecubetower_01").wait_for_completed()
        await self.robot.say_text("Treasure", duration_scalar=3, voice_pitch=0).wait_for_completed()
        await asyncio.sleep(2)
        await self.robot.turn_in_place(cozmo.util.Angle(degrees=180)).wait_for_completed()

    async def get_sad(self):
        await self.robot.go_to_object(self.objects[0], distance_mm(100)).wait_for_completed()
        await self.robot.play_anim_trigger(cozmo.anim.Triggers.RequestGameKeepAwayDeny1).wait_for_completed()
        x = random.randrange(4)
        if x == 0:
            await self.robot.say_text("I miss you father", duration_scalar=2, voice_pitch=0).wait_for_completed()
        elif x == 1:
            await self.robot.say_text("You will always be in my heart, father", duration_scalar=1.5, voice_pitch=0).wait_for_completed()
        elif x == 2:
            await self.robot.say_text("Father", duration_scalar=2, voice_pitch=-1).wait_for_completed()
            await self.robot.say_text("Oh, father", duration_scalar=2, voice_pitch=0).wait_for_completed()
        elif x == 3:
            await self.robot.say_text("What is dead may never die", duration_scalar=2, voice_pitch=-1).wait_for_completed()
        await asyncio.sleep(2)
        await self.robot.turn_in_place(cozmo.util.Angle(degrees=180)).wait_for_completed()

    async def start_program(self):
        await self.robot.set_head_angle(cozmo.util.Angle(degrees=20)).wait_for_completed()
        await self.robot.set_lift_height(0).wait_for_completed()
        self.robot.set_robot_volume(1)
        for i in range(3):
            print(i)
            try:
                self.objects = await self.robot.world.wait_until_observe_num_objects(num=1, object_type=cozmo.objects.LightCube, timeout=60)
            except asyncio.TimeoutError:
                print("Cube not found")
                exit()
            finally:
                self.cube_id[i] = self.objects[0].object_id
                await self.robot.say_text("Ok").wait_for_completed()
                await asyncio.sleep(1)
            self.objects = None
        while True:
            x = random.randrange(self.board_length) - self.board_length/2
            y = random.randrange(self.board_breadth) - self.board_breadth/2
            z = self.robot.pose.position.z
            angle = random.randrange(360)
            pose = cozmo.util.Pose(x, y, z, angle_z=cozmo.util.Angle(degrees=angle))
            await self.robot.go_to_pose(pose).wait_for_completed()
            lookaround = self.robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
            try:
                self.objects = await self.robot.world.wait_until_observe_num_objects(num=1, timeout=10) 
            except asyncio.TimeoutError:
                print("Nothing found")
            lookaround.stop()
            if len(self.objects) == 1:
                if self.objects[0].object_id == self.cube_id[0]:
                    await self.get_scared()
                elif self.objects[0].object_id == self.cube_id[1]:
                    await self.get_sad()
                elif self.objects[0].object_id == self.cube_id[2]:
                    await self.interact_with_treasure()
                else:
                    await self.take_a_nap()
            await asyncio.sleep(0)

    async def run(self, conn):
        asyncio.set_event_loop(conn._loop)
        self.robot = await conn.wait_for_robot()
        await self.start_program()

if __name__ == '__main__':
    CozmoWorld()