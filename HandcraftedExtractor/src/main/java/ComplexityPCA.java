import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.Parameter;
import com.github.javaparser.ast.body.VariableDeclarator;
import com.github.javaparser.ast.expr.*;
import com.github.javaparser.ast.stmt.*;
import com.github.javaparser.ast.type.ClassOrInterfaceType;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.util.Arrays;

public class ComplexityPCA extends VoidVisitorAdapter<Object> {
    private int mLOC, mBlock, mBasicBlock;
    private int mParameter, mLocalVariable, mGlobalVariable;
    private int mLoop, mJump, mDecision, mCondition;
    private int mInstance, mFunctionCall;
    private int mErrorHandler, mThreadHandler;

    ComplexityPCA() {
        mLOC = 0; mBlock = 0; mBasicBlock = 0;
        mParameter = 0; mLocalVariable = 0; mGlobalVariable = 0;
        mLoop = 0; mJump = 0; mDecision = 0; mCondition = 0;
        mInstance = 0; mFunctionCall = 0;
        mErrorHandler = 0; mThreadHandler = 0;
    }

    public String inspectSourceCode(CompilationUnit cu) {
        try {
            this.visit(cu.clone(), null);
            return this.toString();
        } catch (Exception ignore) {
            return "";
        }
    }

    @Override
    public void visit(CompilationUnit cu, Object obj) {
        locateComplexityPCA(cu);
        super.visit(cu, obj);
    }

    private void locateComplexityPCA(CompilationUnit cu) {

        mLOC = cu.findAll(Statement.class).size();

        mBlock = cu.findAll(BlockStmt.class).size();

        mBasicBlock = Common.getBasicBlocks(cu).size();

        mParameter = cu.findAll(Parameter.class).size();

        mLocalVariable = cu.findAll(VariableDeclarator.class).size();

        mGlobalVariable = cu.findAll(SimpleName.class,
                node -> (
                        node.getParentNode().isPresent()
                        && node.getParentNode().get() instanceof NameExpr
                )).size();

        mLoop = cu.findAll(Statement.class,
                stmt -> (
                        stmt instanceof WhileStmt
                        || stmt instanceof DoStmt
                        || stmt instanceof ForStmt
                        || stmt instanceof ForEachStmt
                )).size();

        mJump = cu.findAll(Statement.class,
                stmt -> (
                        stmt instanceof BreakStmt
                        || stmt instanceof ContinueStmt
                        || stmt instanceof ReturnStmt
                )).size();

        mDecision = cu.findAll(IfStmt.class).size()
                + cu.findAll(BlockStmt.class,
                    elseStmt -> (
                                elseStmt.getParentNode().isPresent()
                                && elseStmt.getParentNode().get() instanceof IfStmt
                                && ((IfStmt) elseStmt.getParentNode().get()).getElseStmt().isPresent()
                                && ((IfStmt) elseStmt.getParentNode().get()).getElseStmt().get() == elseStmt
                    )).size()
                + cu.findAll(SwitchEntry.class).size();

        mCondition = cu.findAll(Expression.class,
                stmt -> (
                        stmt instanceof UnaryExpr
                        || stmt instanceof BinaryExpr
                        || stmt instanceof ConditionalExpr
                )).size();

        mInstance = cu.findAll(ObjectCreationExpr.class).size();

        mFunctionCall = cu.findAll(MethodCallExpr.class).size();

        mErrorHandler = cu.findAll(TryStmt.class).size()
                + cu.findAll(CatchClause.class).size()
                + cu.findAll(BlockStmt.class,
                    finallyStmt -> (
                                    finallyStmt.getParentNode().isPresent()
                                    && finallyStmt.getParentNode().get() instanceof TryStmt
                                    && ((TryStmt) finallyStmt.getParentNode().get()).getFinallyBlock().isPresent()
                                    && ((TryStmt) finallyStmt.getParentNode().get()).getFinallyBlock().get() == finallyStmt
                    )).size()
                + cu.findAll(ThrowStmt.class).size();

        mThreadHandler = cu.findAll(ClassOrInterfaceType.class,
                node -> (
                        node.getParentNode().isPresent()
                        && node.getParentNode().get() instanceof ObjectCreationExpr
                        && Arrays.asList("Runnable", "Thread", "Callable").contains(node.getName().toString())
                )).size()
                + cu.findAll(SynchronizedStmt.class).size();
    }

    @Override
    public String toString() {
        return  mLOC + "," + mBlock + "," + mBasicBlock + "," +
                mParameter + "," + mLocalVariable + "," + mGlobalVariable + "," +
                mLoop + "," + mJump + "," + mDecision + "," + mCondition + "," +
                mInstance + "," + mFunctionCall + "," +
                mErrorHandler + "," + mThreadHandler;
    }
}
