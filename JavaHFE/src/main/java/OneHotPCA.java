import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.Parameter;
import com.github.javaparser.ast.expr.*;
import com.github.javaparser.ast.stmt.BlockStmt;
import com.github.javaparser.ast.stmt.ReturnStmt;
import com.github.javaparser.ast.stmt.ThrowStmt;
import com.github.javaparser.ast.stmt.TryStmt;
import com.github.javaparser.ast.type.ClassOrInterfaceType;
import com.github.javaparser.ast.visitor.TreeVisitor;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.io.File;

@SuppressWarnings({"WeakerAccess", "unused"})
public class OneHotPCA extends VoidVisitorAdapter<Object> {
    private static String mMethodName = "OneHotPCA";
    private File mJavaFile = null;
    private String mLabelStr;

    private int mInstanceOf, mBoolean, mEquals, mThis;
    private int mPrintln, mString;
    private int mSuper, mSetUp, mNew, mBuild, mAdd;
    private int mBundle, mOnCreate, mSetContentView, mR;
    private int mToString, mFormat, mStringBuilder, mSbAppend, mStrAppend;
    private int mTaskHandler, mBlock, mError, mMessage;
    private int mHashCode, mTernary;
    private int mInit, mSet, mCreate;
    private int mCmd, mExecute, mResponse, mTryCatchThrow, mThreadHandler;
    private int mReturn, mGet;
    private int mClose, mNull;

    private int mLOC;

    OneHotPCA() {
        mInstanceOf = 0; mBoolean = 0; mEquals = 0; mThis = 0;
        mPrintln = 0; mString = 0;
        mSuper = 0; mSetUp = 0; mNew = 0; mBuild = 0; mAdd = 0;
        mBundle = 0; mOnCreate = 0; mSetContentView = 0; mR = 0;
        mToString = 0; mFormat = 0; mStringBuilder = 0; mSbAppend = 0; mStrAppend = 0;
        mTaskHandler = 0; mBlock = 0; mError = 0; mMessage = 0;
        mHashCode = 0; mTernary = 0;
        mInit = 0; mSet = 0; mCreate = 0;
        mCmd = 0; mExecute = 0; mResponse = 0; mTryCatchThrow = 0; mThreadHandler = 0;
        mReturn = 0; mGet = 0;
        mClose = 0; mNull = 0;
        mLOC = 0; mLabelStr = "";
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
        mLOC = Common.getLOC(cu, mMethodName);
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
                    } else if (node instanceof BlockStmt) {
                        mBlock++;
                    } else if (node instanceof ConditionalExpr
                            && node.toString().contains("?")) {
                        mTernary++;
                    } else if (node instanceof TryStmt || node instanceof ThrowStmt) {
                        mTryCatchThrow++;
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
        } else if (subExpr.equals("Thread")) {
            mThreadHandler++;
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
            mTaskHandler++;
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
        } else if (subExpr.contains("handler")) {
            mThreadHandler++;
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
                mTaskHandler + "," + mBlock + "," + mError + "," + mMessage + "," +
                mHashCode + "," + mTernary + "," +
                mInit + "," + mSet + "," + mCreate + "," +
                mCmd + "," + mExecute + "," + mResponse + "," + mTryCatchThrow + "," + mThreadHandler + "," +
                mReturn + "," + mGet + "," +
                mClose + "," + mNull + "," +
                mLOC;
    }

}
