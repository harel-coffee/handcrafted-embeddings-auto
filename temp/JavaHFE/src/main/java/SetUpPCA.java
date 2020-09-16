import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.expr.*;
import com.github.javaparser.ast.visitor.TreeVisitor;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.io.File;

@SuppressWarnings({"WeakerAccess", "unused"})
public class SetUpPCA extends VoidVisitorAdapter<Object> {
    private static String mMethodName = "setUp";
    private File mJavaFile = null;
    private int mLOC;
    private int mLabelBinary;
    private String mLabelStr;

    private int mSuper, mSetUp, mNew, mBuild, mAdd;

    SetUpPCA() {
        mSuper = 0;
        mSetUp = 0;
        mNew = 0;
        mBuild = 0;
        mAdd = 0;
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
        locateSetUpPCA(cu, obj);
        mLOC = Common.getLOC(cu, mMethodName);
        mLabelBinary = Common.getLabelBinary(mJavaFile, mMethodName);
        mLabelStr = Common.getLabelStr(cu);
        super.visit(cu, obj);
    }

    private void locateSetUpPCA(CompilationUnit cu, Object obj) {
        new TreeVisitor() {
            @Override
            public void process(Node node) {
                try {
                    if (node instanceof SuperExpr) {
                        mSuper++;
                    } else if (node instanceof ObjectCreationExpr
                            && node.toString().startsWith("new")) {
                        mNew++;
                    } else if (node instanceof MethodCallExpr) {
                        String subExpr = ((MethodCallExpr) node).getName().toString();
                        if (subExpr.equals(mMethodName)) {
                            mSetUp++;
                        } else if (subExpr.startsWith("build")) {
                            mBuild++;
                        } else if (subExpr.startsWith("add")) {
                            mAdd++;
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

                mSuper + "," +
                mSetUp + "," +
                mNew + "," +
                mBuild + "," +
                mAdd + "," +

                mLabelBinary;
    }

    public static String getMethodName() {
        return "_" + mMethodName + ".java";
    }
}
