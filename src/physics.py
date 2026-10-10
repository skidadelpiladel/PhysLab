ball = {
    "mass": 2.0,
    "position": 100.0,
    "velocity":50.0,
}
ball2 = {
    "mass": 2.0,
    "position": 300.0,
    "velocity": -50.0,
}
time = 2.0
def new_position(ball, time):
    return ball["position"] + ball["velocity"] * time
ball["position"] = new_position(ball, time)
ball2["position"] = new_position(ball2, time)

print(ball["position"])
print(ball2["position"])
if ball["position"] == ball2["position"]:
    ball["velocity"],ball2["velocity"] = ball2["velocity"], ball["velocity"]
    print("collision detected!")
    print(ball["velocity"])
    print(ball2["velocity"])