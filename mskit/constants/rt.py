import numpy as np
import scipy.stats

from mskit.sequence.fasta import write_fasta


Biognosys_iRT11_FusionSeq = (
    'LGGNEQVTRYILAGVENSKGTFIIDPGGVIRGTFIIDPAAVIRGAGSSEPVTGLDAKTPVISGGPYEYRVEATFGVDESNAKTPVITGAPYEYRDGLDAASYYAPVRADVTPADFSEWSKLFLQFGAQGSPFLK'
)

possible_irt_names = [
    'iRT', 'iRTkit', 'iRT-Kit_WR_fusion',
    'Biognosys standards',
    'sp|iRT|iRT',
    'sp|iRT-Kit_WR_fusion|iRT-Kit_WR_fusion',
    'Biognosys|iRT-Kit_WR_fusion|iRT-Kit_WR_fusion',
]


def generate_irt_fusion_fasta(
        path,
        full_title: str = None,
        prot_db_type: str = 'sp',
        accession: str = 'iRTKitWRFusion',
        entry: str = 'iRTKitWRFusion_iRTKitWRFusion',
        title_desc: str = 'iRTKitWRFusion',
        title_os: str = 'iRTKitWRFusion',
        title_ox: str = '32767',
        title_gn: str = 'iRTKitWRFusion',
        title_pe: str = '1',
        title_sv: str = '1',
):
    if full_title is None:
        full_title = f'>{prot_db_type}|{accession}|{entry} {title_desc} OS={title_os} OX={title_ox} GN={title_gn} PE={title_pe} SV={title_sv}'

    write_fasta({full_title: Biognosys_iRT11_FusionSeq}, file_path=path, seq_line_max_char=None)


"""
From irt-kit-reference-sheet.xls
"""

Biognosys_iRT11 = """\
standard	Q1	iRT	iRT_precise
LGGNEQVTR	487.257	-24.92	-24.916114
GAGSSEPVTGLDAK	644.823	0.00	0.000940333
VEATFGVDESNAK	683.828	12.39	12.38937489
YILAGVENSK	547.298	19.79	19.78791067
TPVISGGPYEYR	669.838	28.71	28.71458122
TPVITGAPYEYR	683.854	33.38	33.381243
DGLDAASYYAPVR	699.339	42.26	42.26388844
ADVTPADFSEWSK	726.836	54.62	54.621042
GTFIIDPGGVIR	622.854	70.52	70.51874133
GTFIIDPAAVIR	636.869	87.23	87.23322233
LFLQFGAQGSPFLK	776.93	100.00	100.0028217\
"""

Biognosys_iRT11_Transitions = """\
Q1 monoisotopic	Q1 average	Q3	relative intensity (approximate, TSQ-Vantage)	rank	precursor charge	fragment type	fragment charge	fragment number	nominal sequence	sequence id	transition id
487.257	487.526	860.423	100	1	2	y	1	8	LGGNEQVTR	iRT Kit_a	LGGNEQVTR.y8.1+
487.257	487.526	503.294	53	2	2	y	1	4	LGGNEQVTR	iRT Kit_a	LGGNEQVTR.y4.1+
487.257	487.526	803.401	50	3	2	y	1	7	LGGNEQVTR	iRT Kit_a	LGGNEQVTR.y7.1+
644.822	645.186	800.452	100	1	2	y	1	8	GAGSSEPVTGLDAK	iRT Kit_b	GAGSSEPVTGLDAK.y8.1+
644.822	645.186	604.331	17	2	2	y	1	6	GAGSSEPVTGLDAK	iRT Kit_b	GAGSSEPVTGLDAK.y6.1+
644.822	645.186	1016.53	16	3	2	y	1	10	GAGSSEPVTGLDAK	iRT Kit_b	GAGSSEPVTGLDAK.y10.1+
683.827	684.22	819.389	100	1	2	b	1	8	VEATFGVDESNAK	iRT Kit_c	VEATFGVDESNAK.b8.1+
683.827	684.22	966.453	56	2	2	y	1	9	VEATFGVDESNAK	iRT Kit_c	VEATFGVDESNAK.y9.1+
683.827	684.22	663.295	46	3	2	y	1	6	VEATFGVDESNAK	iRT Kit_c	VEATFGVDESNAK.y6.1+
547.297	547.62	817.442	100	1	2	y	1	8	YILAGVENSK	iRT Kit_d	YILAGVENSK.y8.1+
547.297	547.62	633.321	54	2	2	y	1	6	YILAGVENSK	iRT Kit_d	YILAGVENSK.y6.1+
547.297	547.62	704.358	52	3	2	y	1	7	YILAGVENSK	iRT Kit_d	YILAGVENSK.y7.1+
669.838	670.237	928.416	100	1	2	y	1	8	TPVISGGPYEYR	iRT Kit_e	TPVISGGPYEYR.y8.1+
669.838	670.237	1041.5	48	2	2	y	1	9	TPVISGGPYEYR	iRT Kit_e	TPVISGGPYEYR.y9.1+
669.838	670.237	841.384	39	3	2	y	1	7	TPVISGGPYEYR	iRT Kit_e	TPVISGGPYEYR.y7.1+
683.853	684.264	956.448	100	1	2	y	1	8	TPVITGAPYEYR	iRT Kit_f	TPVITGAPYEYR.y8.1+
683.853	684.264	855.4	59	2	2	y	1	7	TPVITGAPYEYR	iRT Kit_f	TPVITGAPYEYR.y7.1+
683.853	684.264	1069.53	44	3	2	y	1	9	TPVITGAPYEYR	iRT Kit_f	TPVITGAPYEYR.y9.1+
699.338	699.749	855.436	100	1	2	y	1	7	DGLDAASYYAPVR	iRT Kit_g	DGLDAASYYAPVR.y7.1+
699.338	699.749	926.474	68	2	2	y	1	8	DGLDAASYYAPVR	iRT Kit_g	DGLDAASYYAPVR.y8.1+
699.338	699.749	605.341	58	3	2	y	1	5	DGLDAASYYAPVR	iRT Kit_g	DGLDAASYYAPVR.y5.1+
726.835	727.265	1066.48	100	1	2	y	1	9	ADVTPADFSEWSK	iRT Kit_h	ADVTPADFSEWSK.y9.1+
726.835	727.265	533.746	65	2	2	y	2	9	ADVTPADFSEWSK	iRT Kit_h	ADVTPADFSEWSK.y9.2+
726.835	727.265	584.27	23	3	2	y	2	10	ADVTPADFSEWSK	iRT Kit_h	ADVTPADFSEWSK.y10.2+
622.853	623.225	598.368	100	1	2	y	1	6	GTFIIDPGGVIR	iRT Kit_i	GTFIIDPGGVIR.y6.1+
622.853	623.225	713.395	30	2	2	y	1	7	GTFIIDPGGVIR	iRT Kit_i	GTFIIDPGGVIR.y7.1+
622.853	623.225	826.479	28	3	2	y	1	8	GTFIIDPGGVIR	iRT Kit_i	GTFIIDPGGVIR.y8.1+
636.869	637.251	626.399	100	1	2	y	1	6	GTFIIDPAAVIR	iRT Kit_k	GTFIIDPAAVIR.y6.1+
636.869	637.251	854.51	66	2	2	y	1	8	GTFIIDPAAVIR	iRT Kit_k	GTFIIDPAAVIR.y8.1+
636.869	637.251	741.426	60	3	2	y	1	7	GTFIIDPAAVIR	iRT Kit_k	GTFIIDPAAVIR.y7.1+
776.929	777.412	904.489	100	1	2	y	1	9	LFLQFGAQGSPFLK	iRT Kit_l	LFLQFGAQGSPFLK.y9.1+
776.929	777.412	1051.56	91	2	2	y	1	10	LFLQFGAQGSPFLK	iRT Kit_l	LFLQFGAQGSPFLK.y10.1+
776.929	777.412	504.319	80	3	2	y	1	4	LFLQFGAQGSPFLK	iRT Kit_l	LFLQFGAQGSPFLK.y4.1+\
"""

# irt_to_rt = np.polyfit(df['iRT'], df['RT'], deg=1)
# rt_to_irt = np.polyfit(df['RT'], df['iRT'], deg=1)
# rt_irt_corr = scipy.stats.pearsonr(df['RT'], df['iRT'])
