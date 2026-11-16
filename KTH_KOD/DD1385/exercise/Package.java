// Context
class Package {
    private PackageState state;

    public Package() {
        state = new Ordered(); // starttillstånd
    }

    public void setState(PackageState state) {
        this.state = state;
    }

    public void nextState() {
        state.next(this);
    }

    public void prevState() {
        state.prev(this);
    }

    public void printStatus() {
        state.printStatus();
    }
}
