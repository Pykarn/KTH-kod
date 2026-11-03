import static org.junit.Assert.*;
import org.junit.Test;
import org.junit.*;


public class ShutTheBoxTest {
    ShutTheBox stb;

    @Before
    public void setUp(){
	    stb = new ShutTheBox();

    }
    
    @Test
    public void rollDicesTest(){

	Integer[] dices = stb.rollDices(2);
	//	Integer[] ret=new Integer[]{2,3};
	assertArrayEquals(dices, dices);
    }

    @Test
    public void flippTilesTest(){
	
	//Integer[] dices = stb.flippTiles(selectedTiles, tiles, flippedTiles);
	
	//assertArrayEquals(dices, dices);
    }

    
}
