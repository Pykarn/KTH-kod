class Shipped implements PackageState {
    public void next(Package pkg) {
        pkg.setState(new Delivered());
    }
    public void prev(Package pkg) {
        pkg.setState(new Ordered());
    }
    public void printStatus() {
        System.out.println("Status: Skickat");
    }
}

