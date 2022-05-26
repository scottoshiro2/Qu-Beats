# Qu-Beats v1.0
__by [Scott Oshiro](https://github.com/scottoshiro2), [Tshepang Motsosi](https://github.com/Mabonito)__

_Generating beats with quantum circuits_

[Qiskit Camp Africa](https://community.qiskit.org/events/africa/) project [#33](https://github.com/qiskit-community/qiskit-camp-africa-19/issues/33)

Coaches: [Omar Costa Hamido](https://github.com/omarcostahamido), [Lauren Capelluto](https://github.com/lcapelluto)

presentation slides: https://docs.google.com/presentation/d/1NW7U_GlczXQ9Rn-Ufml5Xie-tFY_vbJgowsy2uo8Ewo

# Qu-Beats v2.0
__by [Scott Oshiro](https://github.com/scottoshiro2)__

_Date: 3/24/2022_

This is similar to the 1st version of Qu-Beats but now you can entangle more complex midi drum patterns and entangle them to generate new patterns. This can run on both the aer-simulator and real quantum computers.

Also one entire drum loop can be considered for each execution of one circuit rather than running the quantum circuit for each subdivision of the midi pattern. (Read Me under construction).

## Steps:
1) Create two midi drum patterns using your favorite Digital Audio Workspace (DAW)
2) Name one of your midi files beat1_input.mid and the other beat2_input.mid
3) run main.py (default is executing on the aer-simulator)
4) There should now be a set of new generated drum midi files. These are variations of your two input drum patterns created in step 1. You can now import them into your DAW to hear and use them in your music project
