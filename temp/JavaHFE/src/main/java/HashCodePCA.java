import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.expr.ConditionalExpr;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.visitor.TreeVisitor;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.io.File;

@SuppressWarnings({"WeakerAccess", "unused"})
public class HashCodePCA extends VoidVisitorAdapter<Object> {
    private static String mMethodName = "hashCode";
    private File mJavaFile = null;
    private int mLOC;
    private int mLabelBinary;
    private String mLabelStr;

    private int mHashCode, mTernary;

    HashCodePCA() {
        mHashCode = 0;
        mTernary = 0;
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
        locateHashCodePCA(cu, obj);
        mLOC = Common.getLOC(cu, mMethodName);
        mLabelBinary = Common.getLabelBinary(mJavaFile, mMethodName);
        mLabelStr = Common.getLabelStr(cu);
        super.visit(cu, obj);
    }

    private void locateHashCodePCA(CompilationUnit cu, Object obj) {
        new TreeVisitor() {
            @Override
            public void process(Node node) {
                try {
                    if (node instanceof MethodCallExpr
                            && ((MethodCallExpr) node).getName().toString().equals(mMethodName)) {
                        mHashCode++;
                    } else if (node instanceof ConditionalExpr
                            && node.toString().contains("?")) {
                        mTernary++;
                    }
                } catch (Exception ignored) {}
            }
        }.visitPreOrder(cu);
    }

    @Override
    public String toString() {
        return mJavaFile + "," +
                mLabelStr + "," +

                mHashCode + "," +
                mTernary + "," +

                mLabelBinary;
    }

    public static String getMethodName() {
        return "_" + mMethodName + ".java";
    }
}
