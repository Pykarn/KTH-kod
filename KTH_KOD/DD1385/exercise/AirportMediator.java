// Fil: AirportMediator.java
public class AirportMediator {


    // --------------------
    // Demo
    // --------------------
    public void runDemo() {
        AirportControlTower tower = new AirportControlTower();

        Aircraft plane1 = new Airplane("Flight-100", tower);
        Aircraft heli1  = new Helicopter("H-7", tower);

        plane1.requestLanding();
        heli1.requestLanding();
        plane1.requestLanding();
    }

    public static void main(String[] args) {
        AirportMediator airport = new AirportMediator();
        airport.runDemo();
    }
}
