// Concrete States
class Ordered implements PackageState {
    public void next(Package pkg) {
        pkg.setState(new Shipped());
    }
    public void prev(Package pkg) {
        System.out.println("Detta paket är redan beställt, inget tidigare steg.");
    }
    public void printStatus() {
        System.out.println("Status: Beställt");
    }
}

