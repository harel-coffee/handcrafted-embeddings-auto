import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.stmt.ThrowStmt;
import com.github.javaparser.ast.stmt.TryStmt;
import com.github.javaparser.ast.type.ClassOrInterfaceType;
import com.github.javaparser.ast.visitor.TreeVisitor;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.io.File;

@SuppressWarnings({"WeakerAccess", "unused"})
public class ExecutePCA extends VoidVisitorAdapter<Object> {
    private static String mMethodName = "execute";
    private File mJavaFile = null;
    private int mLOC;
    private int mLabelBinary;
    private String mLabelStr;

    private int mCmd, mExecute, mResponse, mTryCatchThrow, mThreadHandler;

    ExecutePCA() {
        mCmd = 0;
        mExecute = 0;
        mResponse = 0;
        mTryCatchThrow = 0;
        mThreadHandler = 0;
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
        locateExecutePCA(cu, obj);
        mLOC = Common.getLOC(cu, mMethodName);
        mLabelBinary = Common.getLabelBinary(mJavaFile, mMethodName);
        mLabelStr = Common.getLabelStr(cu);
        super.visit(cu, obj);
    }

    private void locateExecutePCA(CompilationUnit cu, Object obj) {
        new TreeVisitor() {
            @Override
            public void process(Node node) {
                try {
                    if (node instanceof ClassOrInterfaceType
                            && ((ClassOrInterfaceType) node).getName().toString().equals("CommandLine")) {
                        mCmd++;
                    } else if (node instanceof MethodCallExpr) {
                        String subExpr = ((MethodCallExpr) node).getName().toString().toLowerCase();
                        if (subExpr.contains("execut")) {
                            //execute, execution
                            mExecute++;
                        } else if (subExpr.contains("response")) {
                            mResponse++;
                        } else if (subExpr.contains("succe")) {
                            //onSuccess, isSucceeded, SUCCESS
                            mResponse++;
                        } else if (subExpr.contains("fail")) {
                            //onFailure, isFailed, FAILURE
                            mResponse++;
                        } else if (subExpr.contains("handler")) {
                            mThreadHandler++;
                        }
                    } else if (node instanceof TryStmt || node instanceof ThrowStmt) {
                        mTryCatchThrow++;
                    } else if (node instanceof ClassOrInterfaceType
                            && ((ClassOrInterfaceType) node).getName().toString().equals("Thread")) {
                        mThreadHandler++;
                    }
                } catch (Exception ignored) {}
            }
        }.visitPreOrder(cu);
    }

    @Override
    public String toString() {
        return mJavaFile + "," +
                mLabelStr + "," +

                mCmd + "," +
                mExecute + "," +
                mResponse + "," +
                mTryCatchThrow + "," +
                mThreadHandler + "," +

                mLabelBinary;
    }

    public static String getMethodName() {
        return "_" + mMethodName + ".java";
    }
}
