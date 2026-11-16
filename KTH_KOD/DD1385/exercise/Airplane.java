    // --------------------
    // Flygplan
    // --------------------
    public class Airplane extends Aircraft {
        public Airplane(String name, ControlTower tower) {
            super(name, tower);
        }

        @Override
        public void land() {
            System.out.println("Flygplan " + name + " landar.");
        }
    }

