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
    private int mSuperExpr, mMethodCallExpr, mNewObjectCreationExpr, mBuildMethodCallExpr, mAddMethodCallExpr, mLabelBinary;
    private String mLabelStr;

    SetUpPCA() {
        mSuperExpr = 0;
        mMethodCallExpr = 0;
        mNewObjectCreationExpr = 0;
        mBuildMethodCallExpr = 0;
        mAddMethodCallExpr = 0;
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
        mLabelBinary = Common.getLabelBinary(mJavaFile, mMethodName);
        mLabelStr = Common.getLabelStr(cu);
        super.visit(cu, obj);
    }

    private void locateEqualsPCA(CompilationUnit cu, Object obj) {
        new TreeVisitor() {
            @Override
            public void process(Node node) {
                if (node != null) {
                    if (node instanceof SuperExpr) {
                        mSuperExpr++;
                    } else if (node instanceof MethodCallExpr && ((MethodCallExpr) node).getName().toString().equals(mMethodName)){
                        mMethodCallExpr++;
                    } else if (node instanceof ObjectCreationExpr && node.toString().startsWith("new")){
                        mNewObjectCreationExpr++;
                    } else if (node instanceof MethodCallExpr && ((MethodCallExpr) node).getName().toString().startsWith("build")){
                        mBuildMethodCallExpr++;
                    } else if (node instanceof MethodCallExpr && ((MethodCallExpr) node).getName().toString().startsWith("add")){
                        mAddMethodCallExpr++;
                    }
                }
            }
        }.visitPreOrder(cu);
    }

    @Override
    public String toString() {
        return mJavaFile + "," +
                mLabelStr + "," +
                mSuperExpr + "," +
                mMethodCallExpr + "," +
                mNewObjectCreationExpr + "," +
                mBuildMethodCallExpr + "," +
                mAddMethodCallExpr + "," +
                mLabelBinary;
    }

    public static String getMethodName() {
        return "_" + mMethodName + ".java";
    }
}
