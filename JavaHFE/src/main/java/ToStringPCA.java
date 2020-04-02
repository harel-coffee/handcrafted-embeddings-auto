import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.expr.*;
import com.github.javaparser.ast.stmt.ReturnStmt;
import com.github.javaparser.ast.type.ClassOrInterfaceType;
import com.github.javaparser.ast.visitor.TreeVisitor;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.io.File;

@SuppressWarnings({"WeakerAccess", "unused"})
public class ToStringPCA extends VoidVisitorAdapter<Object> {
    private static String mMethodName = "toString";
    private File mJavaFile = null;
    private int mLOC;
    private int mLabelBinary;
    private String mLabelStr;

    private int mToString, mFormat, mStringBuilder, mSbAppend, mStrAppend;

    ToStringPCA() {
        mToString = 0;
        mFormat = 0;
        mStringBuilder = 0;
        mSbAppend = 0;
        mStrAppend = 0;
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
        locateToStringPCA(cu, obj);
        mLOC = Common.getLOC(cu, mMethodName);
        mLabelBinary = Common.getLabelBinary(mJavaFile, mMethodName);
        mLabelStr = Common.getLabelStr(cu);
        super.visit(cu, obj);
    }

    private void locateToStringPCA(CompilationUnit cu, Object obj) {
        new TreeVisitor() {
            @Override
            public void process(Node node) {
                try {
                    if (node instanceof MethodCallExpr) {
                        String subExpr = ((MethodCallExpr) node).getName().toString();
                        if (subExpr.equals(mMethodName)) {
                            mToString++;
                        } else if (subExpr.equals("format")) {
                            mFormat++;
                        } else if (subExpr.equals("append")) {
                            mSbAppend++;
                        }
                    } else if (node instanceof ClassOrInterfaceType
                            && ((ClassOrInterfaceType) node).getName().toString().equals("StringBuilder")) {
                        mStringBuilder++;
                    } else if (node instanceof ReturnStmt) {
                        new TreeVisitor() {
                            @Override
                            public void process(Node node) {
                                if (node instanceof StringLiteralExpr
                                        && node.getParentNode().orElse(null) instanceof BinaryExpr) {
                                    mStrAppend++;
                                }
                            }
                        }.visitPreOrder(node);
                    }
                } catch (Exception ignored) {}
            }
        }.visitPreOrder(cu);
    }

    @Override
    public String toString() {
        return mJavaFile + "," +
                mLabelStr + "," +

                mToString + "," +
                mFormat + "," +
                mStringBuilder + "," +
                mSbAppend + "," +
                mStrAppend + "," +

                mLabelBinary;
    }

    public static String getMethodName() {
        return "_" + mMethodName + ".java";
    }
}
