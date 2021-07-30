from time import sleep


class Animator(object):
    class KeyFrame(object):
        @staticmethod
        def add(divisor, offset=0):
            def wrapper(func):
                func.properties = {"divisor": divisor, "offset": offset, "count": 0}
                return func

            return wrapper

    def __init__(self, delay=0.01):
        self.keyframes = []
        self.frame = 0
        self.delay = delay

        self._register_keyframes()

    def _register_keyframes(self):
        # Some introspection to setup keyframes
        for methodname in dir(self):
            method = getattr(self, methodname)
            if hasattr(method, "properties"):
                self.keyframes.append(method)

    def play(self):
        while True:
            if self.frame < 0:
                continue

            for keyframe in self.keyframes:
                # If divisor == 0 then only run once on first loop
                if self.frame == 0:
                    if keyframe.properties["divisor"] == 0:
                        keyframe(keyframe.properties["count"])
                    else:
                        continue

                # Else perform normal operation
                elif keyframe.properties["divisor"] and not (
                    (self.frame - keyframe.properties["offset"])
                    % keyframe.properties["divisor"]
                ):
                    keyframe(keyframe.properties["count"])
                    keyframe.properties["count"] += 1

            self.frame += 1
            sleep(self.delay)

    def reset_scene(self):
        self.frame = -1


if __name__ == "__main__":

    class Test(Animator):
        @Animator.KeyFrame.add(5, 1)
        def method1(self, frame):
            print(f"method1 {frame}")

        @Animator.KeyFrame.add(1, 1)
        def method2(self, frame):
            print(f"method2 {frame}")

    myclass = Test(1)
    myclass.run()

    while 1:
        sleep(5)
