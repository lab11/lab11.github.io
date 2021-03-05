Harmonia.
=================
Cheap, accurate indoor localization with RF.
--------------------------------------------

Ultra-wideband has been shown to achieve order-cm RF-localization
accuracy, yet it is prohibitively expensive to implement in practice.

Harmonia seeks the best of both worlds, leveraging affordable, low-energy
narrowband frontends with a novel mixing scheme to generate ultra-wideband
(UWB) signals. These signals are captured using a tunable narrowband receiver
that sweeps the spectrum, stitching together a complete UWB picture.

Harmonia is designed as an assymetric _tag_ and _anchor_ system. Lightweight,
low-cost, low-energy, low-complexity tags are distributed in free space.
These tags mix the output of a narrowband radio with a square wave to generate
a UWB signal. Anchor nodes with a highly tunable narrowband frontend quickly
sweep the spectrum and stitch together samples to form one, unified UWB
capture.

Our Harmonia prototype captures 56&nbsp;location samples/second, enabling
location tracking with both high temporal fidelity and high resolution in 3D
space.

[HOMEPAGE_BREAK]

<video controls autoplay style="width: 100%;">
  <source src="Harmonium_Test_Flight.mp4" type="video/mp4">
</video>
