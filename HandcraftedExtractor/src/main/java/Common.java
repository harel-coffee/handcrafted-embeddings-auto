import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.stmt.*;

import java.io.File;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.List;

public class Common {
    public static CompilationUnit getParseUnit(File javaFile) {
        CompilationUnit root = null;
        try {
            String txtCode = new String(Files.readAllBytes(javaFile.toPath()));
            txtCode = "class T { \n" + txtCode + "\n}";
            root = StaticJavaParser.parse(txtCode);
        } catch (Exception ignore) {}
        return root;
    }

    public static String getMethodPath(File javaFile) {
        String method_path = javaFile.toString();
        // to keep the output as csv/tsv file
        method_path = method_path.replaceAll(" ", "_r_space_r_");
        method_path = method_path.replaceAll(",", "_r_comma_r_");
        return method_path;
    }

    public static String getMethodName(CompilationUnit cu) {
        List<MethodDeclaration> methods = cu.findAll(MethodDeclaration.class);
        return methods.get(0).getName().toString();
    }

    public static ArrayList<ArrayList<Statement>> getBasicBlocks(CompilationUnit cu) {
        ArrayList<Statement> innerStmts = new ArrayList<>();
        ArrayList<ArrayList<Statement>> basicBlockStmts = new ArrayList<>();
        ArrayList<Statement> allStatements = (ArrayList<Statement>) cu.findAll(Statement.class);
        for (Statement stmt: allStatements) {
            if (stmt instanceof ExpressionStmt && Common.isPermuteApplicable(stmt)
                    && stmt.findAll(MethodCallExpr.class).size() == 0 ) {
                innerStmts.add(stmt);
            } else {
                if (innerStmts.size() > 1) {
                    basicBlockStmts.add(new ArrayList<>(innerStmts));
                }
                innerStmts.clear();
            }
        }
        return basicBlockStmts;
    }

    public static boolean isPermuteApplicable(Statement stmt) {
        return !(stmt instanceof EmptyStmt || stmt instanceof LabeledStmt || stmt instanceof BreakStmt ||
                        stmt instanceof ContinueStmt || stmt instanceof ReturnStmt);
    }
}
