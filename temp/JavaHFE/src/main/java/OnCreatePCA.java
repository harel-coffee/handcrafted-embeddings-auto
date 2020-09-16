import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.Parameter;
import com.github.javaparser.ast.expr.FieldAccessExpr;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.expr.SuperExpr;
import com.github.javaparser.ast.type.ClassOrInterfaceType;
import com.github.javaparser.ast.visitor.TreeVisitor;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.io.File;

@SuppressWarnings({"WeakerAccess", "unused"})
public class OnCreatePCA extends VoidVisitorAdapter<Object> {
    private static String mMethodName = "onCreate";
    private File mJavaFile = null;
    private int mLOC;
    private int mLabelBinary;
    private String mLabelStr;

    private int mBundle, mSuper, mOnCreate, mSetContentView, mR;

    OnCreatePCA() {
        mBundle = 0;
        mSuper = 0;
        mOnCreate = 0;
        mSetContentView = 0;
        mR = 0;
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
        locateOnCreatePCA(cu, obj);
        mLOC = Common.getLOC(cu, mMethodName);
        mLabelBinary = Common.getLabelBinary(mJavaFile, mMethodName);
        mLabelStr = Common.getLabelStr(cu);
        super.visit(cu, obj);
    }

    private void locateOnCreatePCA(CompilationUnit cu, Object obj) {
        new TreeVisitor() {
            @Override
            public void process(Node node) {
                try{
                    if (node instanceof ClassOrInterfaceType
                            && ((ClassOrInterfaceType) node).getName().toString().equals("Bundle")
                            && node.getParentNode().orElse(null) instanceof Parameter) {
                        mBundle++;
                    } else if (node instanceof SuperExpr) {
                        mSuper++;
                    } else if (node instanceof MethodCallExpr) {
                        String subExpr = ((MethodCallExpr) node).getName().toString();
                        if (subExpr.equals(mMethodName)) {
                            mOnCreate++;
                        } else if (subExpr.equals("setContentView")) {
                            mSetContentView++;
                        }
                    } else if (node instanceof FieldAccessExpr
                            && ((FieldAccessExpr)((FieldAccessExpr) node).getScope()).getScope().toString().equals("R")) {
                        mR++;
                    }
                } catch (Exception ignored) {}
            }
        }.visitPreOrder(cu);
    }

    @Override
    public String toString() {
        return mJavaFile + "," +
                mLabelStr + "," +

                mBundle + "," +
                mSuper + "," +
                mOnCreate + "," +
                mSetContentView + "," +
                mR + "," +

                mLabelBinary;
    }

    public static String getMethodName() {
        return "_" + mMethodName + ".java";
    }
}
