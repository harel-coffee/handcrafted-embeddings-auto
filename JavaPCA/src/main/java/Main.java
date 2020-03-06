public class Main {
    public static void main(String[] args) {
        String inputPath = args[0]; ///scratch/rabin/data/code2vec/pca/tN/...
        String outputPath = args[1]; //data/pca/...
        new ASTExplorer(inputPath, outputPath).call();
    }
}
