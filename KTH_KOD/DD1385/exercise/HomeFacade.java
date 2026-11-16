package facade;

import light.Light;
import tv.TV;
import stereo.Stereo;

public class HomeFacade {
    private Light light;
    private TV tv;
    private Stereo stereo;

    public HomeFacade() {
        light = new Light();
        tv = new TV();
        stereo = new Stereo();
    }

    public void startMovieTime() {
        System.out.println("Förbereder filmkväll...");
        light.turnOff();
        tv.turnOn();
        stereo.turnOn();
    }

    public void endMovieTime() {
        System.out.println("Stänger ner filmkvällen...");
        light.turnOn();
        tv.turnOff();
        stereo.turnOff();
    }
}
