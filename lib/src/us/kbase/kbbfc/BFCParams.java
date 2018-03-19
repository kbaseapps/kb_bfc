
package us.kbase.kbbfc;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: BFCParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "input_reads_upa",
    "workspace_name",
    "output_reads_name",
    "kmer_size",
    "drop_unique_kmer_reads",
    "est_genome_size",
    "est_genome_size_units"
})
public class BFCParams {

    @JsonProperty("input_reads_upa")
    private String inputReadsUpa;
    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("output_reads_name")
    private String outputReadsName;
    @JsonProperty("kmer_size")
    private Long kmerSize;
    @JsonProperty("drop_unique_kmer_reads")
    private Long dropUniqueKmerReads;
    @JsonProperty("est_genome_size")
    private Long estGenomeSize;
    @JsonProperty("est_genome_size_units")
    private String estGenomeSizeUnits;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("input_reads_upa")
    public String getInputReadsUpa() {
        return inputReadsUpa;
    }

    @JsonProperty("input_reads_upa")
    public void setInputReadsUpa(String inputReadsUpa) {
        this.inputReadsUpa = inputReadsUpa;
    }

    public BFCParams withInputReadsUpa(String inputReadsUpa) {
        this.inputReadsUpa = inputReadsUpa;
        return this;
    }

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public BFCParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("output_reads_name")
    public String getOutputReadsName() {
        return outputReadsName;
    }

    @JsonProperty("output_reads_name")
    public void setOutputReadsName(String outputReadsName) {
        this.outputReadsName = outputReadsName;
    }

    public BFCParams withOutputReadsName(String outputReadsName) {
        this.outputReadsName = outputReadsName;
        return this;
    }

    @JsonProperty("kmer_size")
    public Long getKmerSize() {
        return kmerSize;
    }

    @JsonProperty("kmer_size")
    public void setKmerSize(Long kmerSize) {
        this.kmerSize = kmerSize;
    }

    public BFCParams withKmerSize(Long kmerSize) {
        this.kmerSize = kmerSize;
        return this;
    }

    @JsonProperty("drop_unique_kmer_reads")
    public Long getDropUniqueKmerReads() {
        return dropUniqueKmerReads;
    }

    @JsonProperty("drop_unique_kmer_reads")
    public void setDropUniqueKmerReads(Long dropUniqueKmerReads) {
        this.dropUniqueKmerReads = dropUniqueKmerReads;
    }

    public BFCParams withDropUniqueKmerReads(Long dropUniqueKmerReads) {
        this.dropUniqueKmerReads = dropUniqueKmerReads;
        return this;
    }

    @JsonProperty("est_genome_size")
    public Long getEstGenomeSize() {
        return estGenomeSize;
    }

    @JsonProperty("est_genome_size")
    public void setEstGenomeSize(Long estGenomeSize) {
        this.estGenomeSize = estGenomeSize;
    }

    public BFCParams withEstGenomeSize(Long estGenomeSize) {
        this.estGenomeSize = estGenomeSize;
        return this;
    }

    @JsonProperty("est_genome_size_units")
    public String getEstGenomeSizeUnits() {
        return estGenomeSizeUnits;
    }

    @JsonProperty("est_genome_size_units")
    public void setEstGenomeSizeUnits(String estGenomeSizeUnits) {
        this.estGenomeSizeUnits = estGenomeSizeUnits;
    }

    public BFCParams withEstGenomeSizeUnits(String estGenomeSizeUnits) {
        this.estGenomeSizeUnits = estGenomeSizeUnits;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((((((((("BFCParams"+" [inputReadsUpa=")+ inputReadsUpa)+", workspaceName=")+ workspaceName)+", outputReadsName=")+ outputReadsName)+", kmerSize=")+ kmerSize)+", dropUniqueKmerReads=")+ dropUniqueKmerReads)+", estGenomeSize=")+ estGenomeSize)+", estGenomeSizeUnits=")+ estGenomeSizeUnits)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
