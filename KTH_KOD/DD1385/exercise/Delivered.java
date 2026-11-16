class Delivered implements PackageState {
    public void next(Package pkg) {
        System.out.println("Paketet är redan levererat.");
    }
    public void prev(Package pkg) {
        pkg.setState(new Shipped());
    }
    public void printStatus() {
        System.out.println("Status: Levererat");
    }
}
