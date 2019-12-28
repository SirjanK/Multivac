# Multivac: RL Agents that Operate a Smart Phone
Have you ever seen a baby play iphone or Android games before they can 
speak or walk? It's pretty incredible. It's hard to imagine
they have a grasp on what to achieve operating a phone, but 
they become engrossed regardless.

Taking this as some basic inspiration, we look to provide an 
environment and preliminary experiments with launching RL
agents on an Android device. More specifically, the action space 
is 2 dimensional continuous down and up actions on the screen; the observation
space is simply a screenshot of the screen once the action has been taken. The reward
and design of the agent? That's left to experimentation. The project is called Multivac: a name found in
Isaac Asimov's [The Last Question](http://www.physics.princeton.edu/ph115/LQ.pdf).

![Example screen after a "random" agent takes 50 uniformly random clicks on the screen](images/example_screenshot.png)

## Quickstart
Current setup is involved and assumes familiarity with the Android SDK; we are 
currently working on dockerizing this environment for quicker startup.

There are two separate environments to consider:
1. Requirements by the Gym environment and agent side.
2. Requirements on the `jython` side regarding the process that is started using the `monkeyrunner` cmd.

Step by step instructions for setup:
1. Clone the repository locally.
2. Set up a python3.5 virtual environment for the project and activate the environment.
3. Install all requirements listed under `requirements.txt` to this virtualenv.
   This can be done by, `pip install -r requirements.txt`. Once this has been completed,
   setup for the Gym environment and agent side has been complete.
4. Download the Android SDK if not already. There should be the `monkeyrunner` tool under
   `/Sdk/tools/bin/monkeyrunner`. Note the path to the `monkeyrunner` tool,
   denoted `$MONKEYRUNNER_PATH` hereafter.
5. Unzip the `jythonCompatibleRedis.zip` located in this repo. This zip contains
   the `redispy` version `2.10.6` source with some syntax modifications to be
   compatible with `jython`. Note the path to the unzipped source, denoted
   `$REDISPY_PATH` hereafter.
   
Now, here are the instructions for running:
1. Connect an Android device either through USB or open an emulated device through
   Android Studio.
2. Ensure the current working directory is right under `Multivac/` and the virtualenv
from setup is activated. Then, launch the `session_starter.py` script as follows:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)" &&
python session/session_starter.py --monkeyrunner-path $MONKEYRUNNER_PATH --redispy-path $REDISPY_PATH --environment-name $ENV_NAME --agent-name $AGENT_NAME --num-train-steps $NUM_TRAIN_STEPS --num-inference-steps $NUM_INFERENCE_STEPS --observation-delta $OBS_DELTA
```
For a detailed description of all the parameters, run `python session/session_starter.py -h`.
An example to launch a random agent for `50` inference steps using a basic reward function can
be found below:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)" &&
python session/session_starter.py --monkeyrunner-path $MONKEYRUNNER_PATH --redispy-path $REDISPY_PATH --environment-name MeanPixelDifferenceEnv --agent-name random --num-train-steps 10 --num-inference-steps 50 --observation-delta 1000
```

## Design
## Current Rewards and Agents
WIP

Current basic reward is the mean absolute pixel difference between successive frames.

## Contributing
We encourage contributing to improve the current infrastructure along with making
it more robust.

As mentioned in the `Quickstart` section, next step is to dockerize this environment
which will simplify a lot of steps necessary. For the time being, once any changes are made,
run all the tests in the `test` directory using the setup `python3.5` virtual environment.
