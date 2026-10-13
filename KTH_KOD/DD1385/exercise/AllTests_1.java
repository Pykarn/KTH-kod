import org.junit.runner.RunWith;
import org.junit.runners.Suite;

@RunWith(Suite.class)
@Suite.SuiteClasses({
    CalcTest.class,
    CalcTest2.class
})

public class AllTests {
    // ingen kod behövs här, java kommer att ignorera p.g.a @RunWith(Suite.class)
}
