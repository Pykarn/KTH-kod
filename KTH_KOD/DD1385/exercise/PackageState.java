// State interface
interface PackageState {
    void next(Package pkg);
    void prev(Package pkg);
    void printStatus();
}
