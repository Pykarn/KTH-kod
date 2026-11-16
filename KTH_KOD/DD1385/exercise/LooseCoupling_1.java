class Car{
    
    private Person owner;
    private Color color;
    private String brand;

    Car(String brand, Color color){...}

    public void changeGear(int to){...}
    public void fillPetrol(int literPetrol){...}

    
}

class Driver extends Person{
    private Car car;

    
    private String typeOfLicense; 
    Driver (Car car){...}
}

class CarMechanicer extends Person{
    private List cars;
    CarMechanicer(){...}
    void addCarToRepaire(Car car){}
}

//Båda klasserna Driver och CarMechanicer kan anropa repairEngine men man vill inte att Driver ska kunna göra det, då gör vi som nedan:

interface ForDriver{
    public void changeGear(int to){...}
    public void fillPetrol(int literPetrol){...}
}

interface ForMechanicer{
    public void repairEngine(Car car){...}
}


class Driver extends Person implements ForDriver{
    private Car car;
    private String typeOfLicense; 
    Driver (Car car){...}
    public void changeGear(int to){...}
    public void fillPetrol(int literPetrol){...}
    
}

class CarMechanicer extends Person implements ForMechanicer, ForDriver{
    private List cars;
    CarMechanicer(){...}
    void addCarToRepaire(Car car){...}
    public void repairEngine(Car car){...}
    public void changeGear(int to){...}
    public void fillPetrol(int literPetrol){...}
}
