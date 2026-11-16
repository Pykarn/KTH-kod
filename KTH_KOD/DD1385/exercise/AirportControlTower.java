// --------------------
// Flygtorn – Mediator
// --------------------
public class AirportControlTower implements ControlTower {

    private boolean runwayFree = true;

    @Override
    public void requestLanding(Aircraft sender) {
        if (runwayFree) {
            System.out.println("Tornet: Bana ledig. " + sender.name + " får landa.");
            runwayFree = false;
            sender.land();
            runwayFree = true; // Bana fri igen
        } else {
            System.out.println("Tornet: Bana upptagen. " + sender.name + " måste vänta.");
        }
    }
}

