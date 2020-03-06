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
    private int mMethodCallExpr, mFormatMethodCallExpr, mStrAppend, mStringBuilderMethodCallExpr, mAppendMethodCallExpr, mLabelBinary;
    private String mLabelStr;

    ToStringPCA() {
        mMethodCallExpr = 0;
        mFormatMethodCallExpr = 0;
        mStrAppend = 0;
        mStringBuilderMethodCallExpr = 0;
        mAppendMethodCallExpr = 0;
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
                    if (node instanceof MethodCallExpr && ((MethodCallExpr) node).getName().toString().equals(mMethodName)){
                        mMethodCallExpr++;
                    } else if (node instanceof MethodCallExpr && ((MethodCallExpr) node).getName().toString().equals("format")){
                        mFormatMethodCallExpr++;
                    }else if (node instanceof ClassOrInterfaceType && ((ClassOrInterfaceType) node).getName().toString().equals("StringBuilder")){
                        mStringBuilderMethodCallExpr++;
                    } else if (node instanceof MethodCallExpr && ((MethodCallExpr) node).getName().toString().equals("append")){
                        mAppendMethodCallExpr++;
                    } else if (node instanceof ReturnStmt) {
                        new TreeVisitor() {
                            @Override
                            public void process(Node node) {
                                if (node instanceof StringLiteralExpr && node.getParentNode().orElse(null) instanceof BinaryExpr){
                                    mStrAppend++;
                                }
                            }
                        }.visitPreOrder(node);
                    }
                }
            }
        }.visitPreOrder(cu);
    }

    @Override
    public String toString() {
        return mJavaFile + "," +
                mLabelStr + "," +
                mMethodCallExpr + "," +
                mFormatMethodCallExpr + "," +
                mStrAppend + "," +
                mStringBuilderMethodCallExpr + "," +
                mAppendMethodCallExpr + "," +
                mLabelBinary;
    }

    public static String getMethodName() {
        return "_" + mMethodName + ".java";
    }
}
