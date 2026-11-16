// --------------------
// Helikopter
// --------------------
public class Helicopter extends Aircraft {
    public Helicopter(String name, ControlTower tower) {
        super(name, tower);
    }

    @Override
    public void land() {
        System.out.println("Helikopter " + name + " landar.");
    }
}
