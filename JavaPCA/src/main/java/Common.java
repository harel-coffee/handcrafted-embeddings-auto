import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.stmt.*;
import com.github.javaparser.ast.visitor.TreeVisitor;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.StandardOpenOption;
import java.util.List;

@SuppressWarnings({"WeakerAccess", "unused"})
public final class Common {

    static String mRootInputPath = "";
    static String mRootOutputPath = "";

    static CompilationUnit getParseUnit(File javaFile) {
        CompilationUnit root = null;
        try {
            String txtCode = new String(Files.readAllBytes(javaFile.toPath()));
            if(!txtCode.startsWith("class")) txtCode = "class T { \n" + txtCode + "\n}";
            root = StaticJavaParser.parse(txtCode);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return root;
    }

    static void saveEmbedding(String txtEmbedding, String lastPart) {
        try {
            File targetFile = new File(Common.mRootOutputPath + "/" + lastPart + ".csv");
            if (targetFile.getParentFile().exists() || targetFile.getParentFile().mkdirs()) {
                if (targetFile.exists() || targetFile.createNewFile()) {
                    Files.write(targetFile.toPath(),
                            (txtEmbedding + "\n").getBytes(), StandardOpenOption.APPEND);
                }
            }
        } catch (IOException ioEx) {
            ioEx.printStackTrace();
        }
    }

    public static int getLOC(CompilationUnit cu, String methodName) {
        List<MethodDeclaration> mds = cu.findAll(MethodDeclaration.class);
        for(MethodDeclaration md : mds) {
            //if (md.getName().toString().equals(methodName)) {
                List<Statement> stmts = md.findAll(Statement.class);
                return stmts.size() - 1;
            //}

        }
        return 0;
    }

    public static int getLabelBinary(File javaFile, String methodName) {
        return javaFile.getName().endsWith("_" + methodName + ".java") ? 1 : 0;
    }

    public static String getLabelStr(CompilationUnit cu) {
        List<MethodDeclaration> methods = cu.findAll(MethodDeclaration.class);
        return methods.get(0).getName().toString();
    }
}