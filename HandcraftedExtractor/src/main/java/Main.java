import com.github.javaparser.ast.CompilationUnit;
import org.apache.commons.io.FileUtils;

import java.io.File;
import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        if (args.length != 2) {
            System.out.println(
                    "args[0] = Input path to Java folder." + "\n" +
                            "args[1] = Boolean to add complexity features."
            );
            return;
        }

        ArrayList<File> javaFiles = new ArrayList<>(
                FileUtils.listFiles(new File(args[0]), new String[]{"java"}, true)
        );

        System.out.println(args[0] + " : " + javaFiles.size());

        javaFiles.forEach((javaFile) -> {
            String embeddings = ""; //handcrafted_embeddings
            try {
                CompilationUnit cu = Common.getParseUnit(javaFile);
                String method_path = Common.getMethodPath(javaFile);
                String method_name = Common.getMethodName(cu);
                String method_33 = new MethodPCA().inspectSourceCode(cu);
                embeddings = method_path + "," + method_name + "," + method_33;
                if (Boolean.parseBoolean(args[1])) {
                    String complexity_14 = new ComplexityPCA().inspectSourceCode(cu);
                    embeddings += "," + complexity_14;
                }
            } catch (Exception ignore) { }
            System.out.println(embeddings);
        });
    }
}
