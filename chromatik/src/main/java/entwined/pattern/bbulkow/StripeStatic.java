package entwined.pattern.bbulkow;

import heronarts.lx.LX;
import heronarts.lx.model.LXPoint;
import heronarts.lx.parameter.BoundedParameter;
import heronarts.lx.pattern.LXPattern;

public class StripeStatic extends LXPattern {

  // stripes: width in inches
  final BoundedParameter widthParam = new BoundedParameter("WIDTH", 3*12, 12, 20*12);
  final BoundedParameter hue1Param = new BoundedParameter("HUE1", 55, 1, 360);
  final BoundedParameter bright1Param = new BoundedParameter("BRIGHT1", 100, 0, 100);
  final BoundedParameter hue2Param = new BoundedParameter("HUE2", 200, 1, 360);
  final BoundedParameter bright2Param = new BoundedParameter("BRIGHT2", 100, 0, 100);
  final BoundedParameter hue3Param = new BoundedParameter("HUE3", 300, 1, 360);
  final BoundedParameter bright3Param = new BoundedParameter("BRIGHT3", 0, 0, 100);


  public StripeStatic(LX lx) {
    super(lx);
    addParameter("width", widthParam);
    addParameter("hue1", hue1Param);
    addParameter("bright1", bright1Param);
    addParameter("hue2", hue2Param);
    addParameter("bright2", bright2Param);
    addParameter("hue3", hue3Param);
    addParameter("bright3", bright3Param);
  }

  // This is the pattern loop, which will run continuously via LX
  @Override
  public void run(double deltaMs) {
    if (getChannel().fader.getNormalized() == 0) return;
    if (widthParam.getValuef() <= 0) return;

    float[]  hue = new float[3];
    float[] brightness = new float[3];
    int nColors = 0;

    if (bright1Param.getValuef() > 1) {
      hue[nColors] = hue1Param.getValuef();
      brightness[nColors] = bright1Param.getValuef();
      nColors++;
    }
    if (bright2Param.getValuef() > 1) {
      hue[nColors] = hue2Param.getValuef();
      brightness[nColors] = bright2Param.getValuef();
      nColors++;
    }
    if (bright3Param.getValuef() > 1) {
      hue[nColors] = hue3Param.getValuef();
      brightness[nColors] = bright3Param.getValuef();
      nColors++;
    }

    if (nColors == 0) return;

    // Use a for loop here to set the cube colors
    float stripeWidth = widthParam.getValuef();
    for (LXPoint cube : model.points) {
      int ci = (int)(cube.x / stripeWidth) % nColors;
      ci = Math.abs(ci);
      colors[cube.index] = LX.hsb(hue[ci],100,brightness[ci]);
    }

  }
}
