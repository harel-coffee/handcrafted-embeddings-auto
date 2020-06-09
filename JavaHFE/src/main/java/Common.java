import com.github.javaparser.JavaToken;
import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.stmt.*;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.StandardOpenOption;
import java.util.ArrayList;
import java.util.List;

@SuppressWarnings({"WeakerAccess", "unused"})
public final class Common {

    static String ROOT_INPUT_PATH = "";
    static String ROOT_OUTPUT_PATH = "";
    static boolean CLF_MULTI_LEVEL = false;

    static String readJavaCode(File javaFile) {
        String txtCode = "";
        try {
            txtCode = new String(Files.readAllBytes(javaFile.toPath()));
            if(!txtCode.startsWith("class")) txtCode = "class T { \n" + txtCode + "\n}";
        } catch (IOException e) {
            e.printStackTrace();
        }
        return txtCode;
    }

    static CompilationUnit getParseUnit(File javaFile) {
        CompilationUnit root = null;
        try {
            String txtCode = Common.readJavaCode(javaFile);
            root = StaticJavaParser.parse(txtCode);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return root;
    }

    static void saveEmbedding(String txtEmbedding, String lastPart) {
        try {
            File targetFile = new File(Common.ROOT_OUTPUT_PATH + "/" + lastPart + ".csv");
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

    public static ArrayList<ArrayList<Statement>> getBasicBlocks(CompilationUnit cu) {
        ArrayList<Statement> innerStmts = new ArrayList<>();
        ArrayList<ArrayList<Statement>> basicBlockStmts = new ArrayList<>();
        ArrayList<Statement> allStatements = (ArrayList<Statement>) cu.findAll(Statement.class);
        for ( Statement stmt: allStatements) {
            if (stmt instanceof ExpressionStmt
                    && stmt.findAll(MethodCallExpr.class).size() == 0
                    && Common.isPermuteApplicable(stmt)) {
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
        return !(
                stmt instanceof EmptyStmt ||
                stmt instanceof LabeledStmt ||
                stmt instanceof BreakStmt ||
                stmt instanceof ContinueStmt ||
                stmt instanceof ReturnStmt
        );
    }

    public static int getLabelBinary(File javaFile, String methodName) {
        return javaFile.getName().endsWith("_" + methodName + ".java") ? 1 : 0;
    }

    public static int getLabelVal(File javaFile, String methodName) {
        return javaFile.getName().endsWith("_" + methodName + ".java") ? 1 : 0;
    }

    public static String getLabelStr(CompilationUnit cu) {
        List<MethodDeclaration> methods = cu.findAll(MethodDeclaration.class);
        return methods.get(0).getName().toString();
    }

    public static List<JavaToken> getAllTokens (MethodDeclaration md) {
        List<JavaToken> allTokens = new ArrayList<>();
        if (md.getTokenRange().isPresent()) {
            md.getTokenRange().get().forEach(token -> {
                    if (token.getKind() >= JavaToken.Kind.COMMENT_CONTENT.getKind()) {
                        allTokens.add(token);
                    }
                }
            );
        }
        return allTokens;
    }
}