import org.apache.commons.io.FileUtils;

import java.io.File;
import java.util.ArrayList;
import java.util.concurrent.Callable;

public class ASTExplorer implements Callable<Void> {

    ASTExplorer(String inputPath, String outputPath) {
        if (!inputPath.endsWith("/")) {
            inputPath += "/";
        }
        Common.mRootInputPath = inputPath;

        if (!outputPath.endsWith("/")) {
            outputPath += "/";
        }
        Common.mRootOutputPath = outputPath;
    }

    @Override
    public Void call() {
        inspectDataset();
        return null;
    }

    private void inspectDataset() {
        ArrayList<File> javaFiles = new ArrayList<>(
                FileUtils.listFiles(
                        new File(Common.mRootInputPath),
                        new String[]{"java"},
                        true)
        );
        System.out.println(Common.mRootInputPath + " : " + javaFiles.size());

        javaFiles.forEach((javaFile) -> {
            try {
                // for target
                if (javaFile.toString().endsWith(ToStringPCA.getMethodName())) {
                    new ToStringPCA().inspectSourceCode(javaFile);
                } else if (javaFile.toString().endsWith(EqualsPCA.getMethodName())) {
                    new EqualsPCA().inspectSourceCode(javaFile);
                } else if (javaFile.toString().endsWith(SetUpPCA.getMethodName())) {
                    new SetUpPCA().inspectSourceCode(javaFile);
                }

                // for non-target
                if (javaFile.toString().contains("/nonTarget/")) {
                    new ToStringPCA().inspectSourceCode(javaFile);
                    new EqualsPCA().inspectSourceCode(javaFile);
                    new SetUpPCA().inspectSourceCode(javaFile);
                }
            } catch (Exception ex) {
                ex.printStackTrace();
            }
        });
    }
}