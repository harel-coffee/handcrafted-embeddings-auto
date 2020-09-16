import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.visitor.TreeVisitor;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.io.File;

@SuppressWarnings({"WeakerAccess", "unused"})
public class InitPCA extends VoidVisitorAdapter<Object> {
    private static String mMethodName = "init";
    private File mJavaFile = null;
    private int mLOC;
    private int mLabelBinary;
    private String mLabelStr;

    private int mInit, mSet, mCreate;

    InitPCA() {
        mInit = 0;
        mSet = 0;
        mCreate = 0;
        mLOC = 0;
        mLabelBinary = 0;
        mLabelStr = "";
    }

    public void inspectSourceCode(File javaFile) {
        this.mJavaFile = javaFile;
        CompilationUnit root = Common.getParseUnit(mJavaFile);
        if (root != null) {
            this.visit(root.clone(), null);
            Common.saveEmbedding(this.toString(), mMethodName);
        }
    }

    @Override
    public void visit(CompilationUnit cu, Object obj) {
        locateInitPCA(cu, obj);
        mLOC = Common.getLOC(cu, mMethodName);
        mLabelBinary = Common.getLabelBinary(mJavaFile, mMethodName);
        mLabelStr = Common.getLabelStr(cu);
        super.visit(cu, obj);
    }

    private void locateInitPCA(CompilationUnit cu, Object obj) {
        new TreeVisitor() {
            @Override
            public void process(Node node) {
                try {
                    if (node instanceof MethodCallExpr) {
                        String subExpr = ((MethodCallExpr) node).getName().toString();
                        if (subExpr.startsWith("init")) {
                            mInit++;
                        } else if (subExpr.startsWith("set")) {
                            mSet++;
                        } else if (subExpr.toLowerCase().contains("create")) {
                            mCreate++;
                        }
                    }
                } catch (Exception ignored) {}
            }
        }.visitPreOrder(cu);
    }

    @Override
    public String toString() {
        return mJavaFile + "," +
                mLabelStr + "," +

                mInit + "," +
                mSet + "," +
                mCreate + "," +

                mLabelBinary;
    }

    public static String getMethodName() {
        return "_" + mMethodName + ".java";
    }
}
