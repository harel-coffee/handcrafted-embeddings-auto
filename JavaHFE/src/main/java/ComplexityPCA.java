import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.body.Parameter;
import com.github.javaparser.ast.body.VariableDeclarator;
import com.github.javaparser.ast.expr.*;
import com.github.javaparser.ast.stmt.*;
import com.github.javaparser.ast.type.ClassOrInterfaceType;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;
import fr.inria.controlflow.ControlFlowBuilder;
import fr.inria.controlflow.ControlFlowGraph;
import spoon.Launcher;
import spoon.reflect.declaration.CtElement;
import spoon.support.reflect.declaration.CtMethodImpl;

import java.io.File;
import java.util.Arrays;

@SuppressWarnings({"WeakerAccess", "unused"})
public class ComplexityPCA extends VoidVisitorAdapter<Object> {
    private final String mMethodName = "ComplexityPCA";
    private File mJavaFile = null;
    private String mLabelStr;

    private int mLOC, mBlock, mBasicBlock;
    private int mParameter, mLocalVariable, mGlobalVariable;
    private int mLoop, mJump, mDecision, mCondition;
    private int mInstance, mFunctionCall;
    private int mErrorHandler, mThreadHandler;
    private int mASTNode, mASTToken;
    private int mCFGStmt, mCFGBCond;

    ComplexityPCA() {
        mLOC = 0; mBlock = 0; mBasicBlock = 0;
        mParameter = 0; mLocalVariable = 0; mGlobalVariable = 0;
        mLoop = 0; mJump = 0; mDecision = 0; mCondition = 0;
        mInstance = 0; mFunctionCall = 0;
        mErrorHandler = 0; mThreadHandler = 0;
        mASTNode = 0; mASTToken = 0;
        mCFGStmt = 0; mCFGBCond = 0;
        mLabelStr = "";
    }

    public void inspectSourceCode(File javaFile) {
        this.mJavaFile = javaFile;
        CompilationUnit root = Common.getParseUnit(mJavaFile);
        if (root != null) {
            this.visit(root.clone(), null);
            Common.saveEmbedding(this.toString(), mMethodName);
            System.out.println(this.toString());
        }
    }

    @Override
    public void visit(CompilationUnit cu, Object obj) {
        complexityASTParser(cu);
        complexitySpoonCFG();
        mLabelStr = Common.getLabelStr(cu);
        super.visit(cu, obj);
    }

    private void complexityASTParser(CompilationUnit cu) {

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

        MethodDeclaration md = cu.findAll(MethodDeclaration.class).get(0);
        mASTNode = md.findAll(Node.class).size();
        mASTToken = Common.getAllTokens(md).size();
    }

    private void complexitySpoonCFG() {
        String content = Common.readJavaCode(mJavaFile);
        Iterable<CtElement> ctElements = Launcher.parseClass(content).asIterable();
        for (CtElement ctElement: ctElements) {
            if (!(ctElement instanceof CtMethodImpl)) {
                continue;
            }
            ControlFlowBuilder builder = new ControlFlowBuilder();
            ControlFlowGraph graph = builder.build(ctElement);
            mCFGStmt = graph.statementCount();
            mCFGBCond = graph.branchCount();
            break;
        }
    }

    @Override
    public String toString() {
        return mJavaFile + "," +
                mLabelStr + "," +
                mLOC + "," + mBlock + "," + mBasicBlock + "," +
                mParameter + "," + mLocalVariable + "," + mGlobalVariable + "," +
                mLoop + "," + mJump + "," + mDecision + "," + mCondition + "," +
                mInstance + "," + mFunctionCall + "," +
                mErrorHandler + "," + mThreadHandler + "," +
                mASTNode + "," + mASTToken + "," +
                mCFGStmt + "," + mCFGBCond;
    }
}
