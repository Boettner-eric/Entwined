package entwined.pattern.colin_hunt;

import heronarts.lx.LX;
import heronarts.lx.model.LXPoint;
import heronarts.lx.modulator.SawLFO;
import heronarts.lx.parameter.BoundedParameter;
import heronarts.lx.pattern.LXPattern;

import entwined.utils.EntwinedUtils;

/**
An RGB wave that covers the whole field.
*/
public class ColorWave extends LXPattern {

  // Variable Declarations go here
  private float minz = Float.MAX_VALUE;
  private float maxz = -Float.MAX_VALUE;
  // private float waveWidth = 1;
  private float speedMult = 1000;

  final BoundedParameter speedParam = new BoundedParameter("Speed", 5, 20, .01);
  final BoundedParameter waveSlope = new BoundedParameter("waveSlope", 360, 1, 720);
  final SawLFO wave = new SawLFO(0, 360, speedParam.getValuef() * speedMult);

  // add speed, wave width

  // Constructor and initial setup
  // Remember to use addParameter and addModulator if you're using Parameters or sin waves
  public ColorWave(LX lx) {
    super(lx);
    addModulator(wave).start();
    addParameter("waveslope", waveSlope);
    addParameter("speed", speedParam);

    for (LXPoint cube : model.points) {
      if (cube.z < minz) {minz = cube.z;}
      if (cube.z > maxz) {maxz = cube.z;}
    }
  }

  // This is the pattern loop, which will run continuously via LX
  @Override
  public void run(double deltaMs) {
    if (getChannel().fader.getNormalized() == 0) return;

    wave.setPeriod(speedParam.getValuef() * speedMult);

    // Use a for loop here to set the cube colors
    for (LXPoint cube : model.points) {
      // XXX - don't know what Utils.map() used to do.
      colors[cube.index] = LX.hsb( (wave.getValuef() + waveSlope.getValuef() * EntwinedUtils.map(cube.z, minz, maxz) ) % 360, 100, 100);
    }
  }
}
