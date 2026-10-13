/*import org.junit.After;
import org.junit.Before;
import org.junit.BeforeClass;*/
import org.junit.Test;
import static org.junit.Assert.*;


public class CalcTest{


    @Test
    public void testAdd(){
	Calc c= new Calc();
	assertEquals(5, c.add(2,3));
    }


    @Test
    public void testDiv(){
	Calc c= new Calc();
	assertEquals(0.6 , c.div(6,5),0.5);
    }


}
