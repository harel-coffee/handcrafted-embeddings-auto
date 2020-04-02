import org.apache.commons.io.FileUtils;

import java.io.File;
import java.util.ArrayList;
import java.util.concurrent.Callable;

public class ASTExplorer implements Callable<Void> {

    ASTExplorer(String inputPath, String outputPath, Boolean clfMultilevel) {
        if (!inputPath.endsWith("/")) {
            inputPath += "/";
        }
        Common.ROOT_INPUT_PATH = inputPath;

        if (!outputPath.endsWith("/")) {
            outputPath += "/";
        }
        Common.ROOT_OUTPUT_PATH = outputPath;

        Common.CLF_MULTI_LEVEL = clfMultilevel;
    }

    @Override
    public Void call() {
        inspectDataset();
        return null;
    }

    private void inspectDataset() {
        ArrayList<File> javaFiles = new ArrayList<>(
                FileUtils.listFiles(
                        new File(Common.ROOT_INPUT_PATH),
                        new String[]{"java"},
                        true)
        );
        System.out.println(Common.ROOT_INPUT_PATH + " : " + javaFiles.size());

        javaFiles.forEach((javaFile) -> {
            try {
                if (Common.CLF_MULTI_LEVEL) {
                    // multilevel classifier
                    new OneHotPCA().inspectSourceCode(javaFile);
                } else {
                    binaryClf(javaFile);
                }

            } catch (Exception ex) {
                ex.printStackTrace();
            }
        });
    }

    private void binaryClf(File javaFile) {
        // for target
        if (javaFile.toString().endsWith(EqualsPCA.getMethodName())) {
            new EqualsPCA().inspectSourceCode(javaFile);
        } else if (javaFile.toString().endsWith(MainPCA.getMethodName())) {
            new MainPCA().inspectSourceCode(javaFile);
        } else if (javaFile.toString().endsWith(SetUpPCA.getMethodName())) {
            new SetUpPCA().inspectSourceCode(javaFile);
        } else if (javaFile.toString().endsWith(OnCreatePCA.getMethodName())) {
            new OnCreatePCA().inspectSourceCode(javaFile);
        } else if (javaFile.toString().endsWith(ToStringPCA.getMethodName())) {
            new ToStringPCA().inspectSourceCode(javaFile);
        } else if (javaFile.toString().endsWith(RunPCA.getMethodName())) {
            new RunPCA().inspectSourceCode(javaFile);
        } else if (javaFile.toString().endsWith(HashCodePCA.getMethodName())) {
            new HashCodePCA().inspectSourceCode(javaFile);
        } else if (javaFile.toString().endsWith(InitPCA.getMethodName())) {
            new InitPCA().inspectSourceCode(javaFile);
        } else if (javaFile.toString().endsWith(ExecutePCA.getMethodName())) {
            new ExecutePCA().inspectSourceCode(javaFile);
        } else if (javaFile.toString().endsWith(GetPCA.getMethodName())) {
            new GetPCA().inspectSourceCode(javaFile);
        } else if (javaFile.toString().endsWith(ClosePCA.getMethodName())) {
            new ClosePCA().inspectSourceCode(javaFile);
        }

        // for non-target
        if (javaFile.toString().contains("/nonTarget/")) {
            new EqualsPCA().inspectSourceCode(javaFile);
            new MainPCA().inspectSourceCode(javaFile);
            new SetUpPCA().inspectSourceCode(javaFile);
            new OnCreatePCA().inspectSourceCode(javaFile);
            new ToStringPCA().inspectSourceCode(javaFile);
            new RunPCA().inspectSourceCode(javaFile);
            new HashCodePCA().inspectSourceCode(javaFile);
            new InitPCA().inspectSourceCode(javaFile);
            new ExecutePCA().inspectSourceCode(javaFile);
            new GetPCA().inspectSourceCode(javaFile);
            new ClosePCA().inspectSourceCode(javaFile);
        }
    }
}