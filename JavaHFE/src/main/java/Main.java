public class Main {
    public static void main(String[] args) {
        String inputPath = args[0]; ///scratch/rabin/data/code2vec/pca/tN/...
        String outputPath = args[1]; //data/pca/...
        boolean clfMultilevel = false;
        if (args.length > 2) {
            clfMultilevel = Boolean.parseBoolean(args[2]); //true=multi-level/false=binary
        }
        new ASTExplorer(inputPath, outputPath, clfMultilevel).call();
    }
}
