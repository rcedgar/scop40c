## SCOP40c: curated SCOP40

For accuracy benchmarking of structure homology search and training of a null model, an ideal structure classification should achieve a balance between false-positive and false-negative homology assignments, so that the measured distribution of false-positive scores according to the reference is close to correct despite the inevitable errors that will be present in the database. This goal conflicts with a conservative approach where structures are assigned to the same superfamily only when there is convincing evidence of homology. 

SCOP40c is a curated subset of SCOP40 v1.75 where, we believe, homology better corresponds to superfamilies. In our judgment, SCOP40c is preferable to SCOP40 for training a null model and for assessing homology detection accuracy.

The subset is defined in this file:

<pre>
final_analysis/scop40c.lookup
</pre>

This is a tab-separated text file (165 kb) with one domain per line plus the SCOP family assignment, like this:

<pre>
d1n1ba1 a.102.4.1
d1m45a_ a.39.1.5
d1k1xa1 a.8.3.2
d1ogad2 b.1.1.2
...
</pre>

You can download the structure files for all of SCOP40 v1.75 like this:

<pre>
wget https://wwwuser.gwdg.de/~compbiol/foldseek/scop40pdb.tar.gz
</pre>

### Analysis pipline to reconstruct scop40c.lookup

<pre>
cd bash
./run_2025-05-21_complete_with_top_fps_final_analysis4.bash
</pre>

### Examples of different SCOP folds with clear homology

[<img width=600 height=600 src="https://raw.githubusercontent.com/rcedgar/scop40c/refs/heads/main/manual_analysis_b68_b69_b70/b68_69_70_figure.svg" width="150">](manual_analysis_b68_b69_b70/b68_69_70_figure.svg)

**Folds b.68, b.69 and b.70** 

Domains with similarity in both structure and sequence which are classified to three different folds by SCOP. All three folds are beta-propellers, distinguished by the number of blades in the propeller: six in fold `b.68`, seven in `b.69` and eight in `b.68`. Two pair-wise BLASTP alignments are shown, both of which have 38% sequence identity between different folds and highly significant E-values 4E-5 and 3E-4, respectively (E-values calculated assuming a database of SCOP40 size). The sequence motif `WSPDG` is well-conserved across all folds; the sequence logo shown here was obtained from a Muscle-3D multiple structure alignment for domains in all three folds. A conserved `P` is exposed at the turn in a beta hairpin which connects two blades in the propeller. These folds, and other folds having high-confidence homology, are removed from the curated reference SCOP40c.
<br/>
<br/>

[<img width=600 height=600 src="https://raw.githubusercontent.com/rcedgar/scop40c/refs/heads/main/manual_analysis_c.1_c.2_c.3/c.1_c.2_c.3_figure.svg" width="150">](manual_analysis_b68_b69_b70/b68_69_70_figure.svg)

**Folds c.1, c.2 and c.3**

<small>
Another example where clearly homologous domains are classified by SCOP to different folds.
</small>
