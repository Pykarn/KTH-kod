// --------------------
// Abstrakt komponent
// --------------------
public abstract class Aircraft {
    protected ControlTower tower;
    protected String name;

    public Aircraft(String name, ControlTower tower) {
        this.name = name;
        this.tower = tower;
    }

    public void requestLanding() {
        System.out.println(name + ": Begär landning.");
        tower.requestLanding(this);
    }

    public abstract void land();
}
