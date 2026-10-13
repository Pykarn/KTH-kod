/*import org.junit.After;
import org.junit.Before;
import org.junit.BeforeClass;*/
import org.junit.Test;
import static org.junit.Assert.*;


public class CalcTest2{


    @Test
    public void testSub(){
	Calc2 c= new Calc2();
	assertEquals(-1, c.sub(2,3));
    }


    @Test
    public void testMul(){
	Calc2 c= new Calc2();
	assertEquals(30 , c.mul(6,5));
    }
    

}
