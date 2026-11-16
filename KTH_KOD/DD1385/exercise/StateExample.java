public class StateExample {
    public static void main(String[] args) {
        Package pkg = new Package();
        pkg.printStatus();  // Beställt
        pkg.nextState();
        pkg.printStatus();  // Skickat
        pkg.nextState();
        pkg.printStatus();  // Levererat
        pkg.prevState();
        pkg.printStatus();  // Skickat
    }
}
