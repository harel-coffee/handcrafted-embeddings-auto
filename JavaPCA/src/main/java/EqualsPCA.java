import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.expr.BooleanLiteralExpr;
import com.github.javaparser.ast.expr.InstanceOfExpr;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.expr.ThisExpr;
import com.github.javaparser.ast.visitor.TreeVisitor;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.io.File;

@SuppressWarnings({"WeakerAccess", "unused"})
public class EqualsPCA extends VoidVisitorAdapter<Object> {
    private static String mMethodName = "equals";
    private File mJavaFile = null;
    private int mInstanceOfExpr, mBooleanLiteralExpr, mMethodCallExpr, mThisExpr, mLOC, mLabelBinary;
    private String mLabelStr;

    EqualsPCA() {
        mInstanceOfExpr = 0;
        mBooleanLiteralExpr = 0;
        mMethodCallExpr = 0;
        mThisExpr = 0;
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
        locateEqualsPCA(cu, obj);
        mLOC = Common.getLOC(cu, mMethodName);
        mLabelBinary = Common.getLabelBinary(mJavaFile, mMethodName);
        mLabelStr = Common.getLabelStr(cu);
        super.visit(cu, obj);
    }

    private void locateEqualsPCA(CompilationUnit cu, Object obj) {
        new TreeVisitor() {
            @Override
            public void process(Node node) {
                if (node != null) {
                    if (node instanceof InstanceOfExpr) {
                        mInstanceOfExpr++;
                    } else if (node instanceof BooleanLiteralExpr) {
                        mBooleanLiteralExpr++;
                    } else if (node instanceof MethodCallExpr && ((MethodCallExpr) node).getName().toString().equals(mMethodName)){
                        mMethodCallExpr++;
                    } else if (node instanceof ThisExpr){
                        mThisExpr++;
                    }
                }
            }
        }.visitPreOrder(cu);
    }

    @Override
    public String toString() {
        return mJavaFile + "," +
                mLabelStr + "," +
                mInstanceOfExpr + "," +
                mBooleanLiteralExpr + "," +
                mMethodCallExpr + "," +
                mThisExpr + "," +
                mLOC + "," +
                mLabelBinary;
    }

    public static String getMethodName() {
        return "_" + mMethodName + ".java";
    }
}
