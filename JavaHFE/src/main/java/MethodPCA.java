import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.Parameter;
import com.github.javaparser.ast.expr.*;
import com.github.javaparser.ast.stmt.ReturnStmt;
import com.github.javaparser.ast.type.ClassOrInterfaceType;
import com.github.javaparser.ast.visitor.TreeVisitor;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.io.File;
@SuppressWarnings({"WeakerAccess", "unused"})
public class MethodPCA extends VoidVisitorAdapter<Object> {
    private final String mMethodName = "MethodPCA";
    private File mJavaFile = null;
    private String mLabelStr;

    private int mInstanceOf, mBoolean, mEquals, mThis;
    private int mPrintln, mString;
    private int mSuper, mSetUp, mNew, mBuild, mAdd;
    private int mBundle, mOnCreate, mSetContentView, mR;
    private int mToString, mFormat, mStringBuilder, mSbAppend, mStrAppend;
    private int mTask, mError, mMessage;
    private int mHashCode, mTernary;
    private int mInit, mSet, mCreate;
    private int mCmd, mExecute, mResponse;
    private int mReturn, mGet;
    private int mClose, mNull;

    MethodPCA() {
        mInstanceOf = 0; mBoolean = 0; mEquals = 0; mThis = 0;
        mPrintln = 0; mString = 0;
        mSuper = 0; mSetUp = 0; mNew = 0; mBuild = 0; mAdd = 0;
        mBundle = 0; mOnCreate = 0; mSetContentView = 0; mR = 0;
        mToString = 0; mFormat = 0; mStringBuilder = 0; mSbAppend = 0; mStrAppend = 0;
        mTask = 0; mError = 0; mMessage = 0;
        mHashCode = 0; mTernary = 0;
        mInit = 0; mSet = 0; mCreate = 0;
        mCmd = 0; mExecute = 0; mResponse = 0;
        mReturn = 0; mGet = 0;
        mClose = 0; mNull = 0;
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
        locateOneHotPCA(cu, obj);
        mLabelStr = Common.getLabelStr(cu);
        super.visit(cu, obj);
    }

    private void locateOneHotPCA(CompilationUnit cu, Object obj) {
        new TreeVisitor() {
            @Override
            public void process(Node node) {
                try {
                    if (node instanceof InstanceOfExpr) {
                        mInstanceOf++;
                    } else if (node instanceof BooleanLiteralExpr) {
                        mBoolean++;
                    } else if (node instanceof MethodCallExpr) {
                        locateMethodCall((MethodCallExpr) node);
                    } else if (node instanceof ThisExpr) {
                        mThis++;
                    } else if (node instanceof ClassOrInterfaceType) {
                        locateClassOrInterface((ClassOrInterfaceType) node);
                    } else if (node instanceof SuperExpr) {
                        mSuper++;
                    } else if (node instanceof ObjectCreationExpr
                            && node.toString().startsWith("new")) {
                        mNew++;
                    } else if (node instanceof FieldAccessExpr
                            && ((FieldAccessExpr)((FieldAccessExpr) node).getScope()).getScope().toString().equals("R")) {
                        mR++;
                    } else if (node instanceof ReturnStmt) {
                        mReturn++;
                        new TreeVisitor() {
                            @Override
                            public void process(Node node) {
                                if (node instanceof StringLiteralExpr
                                        && node.getParentNode().orElse(null) instanceof BinaryExpr) {
                                    mStrAppend++;
                                }
                            }
                        }.visitPreOrder(node);
                    } else if (node instanceof ConditionalExpr
                            && node.toString().contains("?")) {
                        mTernary++;
                    } else if (node instanceof NullLiteralExpr) {
                        mNull++;
                    }
                } catch (Exception ignored) {}
            }
        }.visitPreOrder(cu);
    }

    private void locateClassOrInterface(ClassOrInterfaceType node) {
        String subExpr = node.getName().toString();
        if (subExpr.equals("String")) {
            mString++;
        } else if (subExpr.equals("Bundle")
                && node.getParentNode().orElse(null) instanceof Parameter) {
            mBundle++;
        } else if(subExpr.equals("StringBuilder")) {
            mStringBuilder++;
        } else if (subExpr.equals("CommandLine")) {
            mCmd++;
        }
    }

    private void locateMethodCall(MethodCallExpr node) {
        String subExpr = node.getName().toString().toLowerCase();
        if (subExpr.equals("equals")) {
            mEquals++;
        } else if (subExpr.contains("println")) {
            mPrintln++;
        } else if (subExpr.equals("setup")) {
            mSetUp++;
        } else if (subExpr.startsWith("build")) {
            mBuild++;
        } else if (subExpr.startsWith("add")) {
            mAdd++;
        } else if (subExpr.equals("oncreate")) {
            mOnCreate++;
        } else if (subExpr.equals("setcontentview")) {
            mSetContentView++;
        } else if (subExpr.equals("tostring")) {
            mToString++;
        } else if (subExpr.equals("format")) {
            mFormat++;
        } else if (subExpr.equals("append")) {
            mSbAppend++;
        } else if (subExpr.contains("task") || subExpr.contains("handler")) {
            mTask++;
        } else if (subExpr.contains("error")) {
            mError++;
        } else if (subExpr.contains("message")) {
            mMessage++;
        } else if (subExpr.equals("hashcode")) {
            mHashCode++;
        } else if (subExpr.startsWith("init")) {
            mInit++;
        } else if (subExpr.startsWith("set")) {
            mSet++;
        } else if (subExpr.toLowerCase().contains("create")) {
            mCreate++;
        } else if (subExpr.contains("execut")) {
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
        } else if (subExpr.startsWith("get")) {
            mGet++;
        } else if (subExpr.equals("close")) {
            mClose++;
        }
    }

    @Override
    public String toString() {
        return mJavaFile + "," +
                mLabelStr + "," +
                mInstanceOf + "," + mBoolean + "," + mEquals + "," + mThis + "," +
                mPrintln + "," + mString + "," +
                mSuper + "," + mSetUp + "," + mNew + "," + mBuild + "," + mAdd + "," +
                mBundle + "," + mOnCreate + "," + mSetContentView + "," + mR + "," +
                mToString + "," + mFormat + "," + mStringBuilder + "," + mSbAppend + "," + mStrAppend + "," +
                mTask + "," + mError + "," + mMessage + "," +
                mHashCode + "," + mTernary + "," +
                mInit + "," + mSet + "," + mCreate + "," +
                mCmd + "," + mExecute + "," + mResponse + "," +
                mReturn + "," + mGet + "," +
                mClose + "," + mNull ;
    }

}
