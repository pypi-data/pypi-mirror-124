# -*- coding: utf-8 -*-
import sys
import gffutils
import pandas as pd 
from Bio.Seq import Seq
from collections import defaultdict
from featurExtract.utils.util import utr3_type, utr5_type, mRNA_type
from featurExtract.utils.util import stop_codon_seq, add_stop_codon

# table header 
['TranscriptID','Chrom', 'Strand','CDS Interval','uORF Start','uORF End','uORF Type','uORF Length','uORF']



def uorf(transcript_id, chrom, strand, matural_transcript, coding_sequence):
    '''
    parameters:
     transcript_id:      transcript id
     matural_transcript: a Seq type (Biopython) from mature transcript without intron
     coding_sequence:    a Seq type (Biopython) from coding sequence start with ATG , 
                         end with TAA, TGA, TAG
    return:
     upper stream open reading frame
    '''
    uORF_dict = defaultdict(list)
    stop_codon_list = ['TAA','TAG','TGA']
    # start_codon means the first base position in matural_transcript
    start_codon = matural_transcript.index(coding_sequence)
    # stop_codon means the last base position in matural transcript
    cds_len = len(coding_sequence)
    stop_codon = start_codon + cds_len
    cds_intervel = str(start_codon) + '-' + str(stop_codon)
    mt_len = len(matural_transcript)
    utr5 = matural_transcript[:start_codon]
    utr5_len = len(utr5)
    utr3 = matural_transcript[stop_codon:]
    for i in range(0, utr5_len-3+1):
        # start codon find 
        if matural_transcript[i:i+3] == "ATG":
            for j in range(i+3,stop_codon,3):
            # stop codon find
                if matural_transcript[j:j+3] in stop_codon_list and j < utr5_len:
                    # type1 uORF  upstream; not unique 
                    type1_uORF = matural_transcript[i:j+3]
                    out1 = [transcript_id, chrom, strand, cds_intervel, i+1, j+3, 'type1', len(type1_uORF), type1_uORF]
                    if not uORF_dict.get('type1_uORF'):
                        uORF_dict['type1_uORF'] = [out1]
                    else:
                        uORF_dict['type1_uORF'].append(out1)
                    break 
                if matural_transcript[j:j+3] in stop_codon_list and j + 3 > utr5_len and j + 3 < stop_codon:
                    # type2 uORF across; the overlap region is triple or not; not unique
                    type2_uORF = matural_transcript[i:j+3]
                    out2 = [transcript_id, chrom, strand, cds_intervel, i+1, j+3, 'type2', len(type2_uORF), type2_uORF]
                    if not uORF_dict.get('type2_uORF'):
                        uORF_dict['type2_uORF'] = [out2]
                    else:
                        uORF_dict['type2_uORF'].append(out2)
                    break 
                if matural_transcript[j:j+3] in stop_codon_list and j + 3 > utr5_len and j+3 == stop_codon and (utr5_len - i)%3 == 0:
                    # N extention 通读; not unique 
                    type3_uORF = matural_transcript[i:utr5_len+cds_len]
                    out3 = [transcript_id, chrom, strand, cds_intervel, i+1, j+3, 'type3', len(type3_uORF), type3_uORF]
                    if not uORF_dict.get('type3_uORF'):
                        uORF_dict['type3_uORF'] = [out3]
                    else:
                        uORF_dict['type3_uORF'].append(out3)
                    break
    return uORF_dict



def get_uorf(args):
    '''
    parameters:
        args: parse from argparse
    return:
        elements write to a file or stdout
    '''
    db = gffutils.FeatureDB(args.database, keep_order=True)
    
    uORF_seq = pd.DataFrame(columns=['TranscriptID','Chrom','Strand','CDS Interval','uORF Start','uORF End','uORF Type','uORF Length','uORF'])
    index = 0
    mRNA_str = mRNA_type(args.style) 
    if not args.transcript:
        for t in db.features_of_type(mRNA_str, order_by='start'):
            # primary transcript (pt) 是基因组上的转录本的序列，
            # 有的会包括intron，所以提取的序列和matural transcript 不一致
            # print(t)
            pt = t.sequence(args.genome, use_strand=True)
            # matural transcript (mt)
            # exon 提取的是转录本内成熟的MRNA的序列,即外显子收尾相连的matural transcript
            mt = ''
            for e in db.children(t, featuretype='exon', order_by='start'):
                s = e.sequence(args.genome, use_strand=False) # 不反向互补，对于负链要得到全部的cds后再一次性反向互补
                mt += s
            mt = Seq(mt)
            if t.strand == '-':
                mt = mt.reverse_complement()
            # CDS 提取的是编码区 ATG ... TAG
            cds = ''
            for c in db.children(t, featuretype='CDS', order_by='start'):
                #print(c)
                s = c.sequence(args.genome, use_strand=False) # 不反向互补，对于负链要得到全部的cds后再一次性反向互补
                cds += s
            if args.style == 'GTF':
                sc_seq = stop_codon_seq(db, t, args.genome)
                cds = add_stop_codon(cds, t.strand, sc_seq)
            cds = Seq(cds)
            if t.strand == '-':
                cds = cds.reverse_complement()
            uORF_dict = uorf(t.id, t.chrom, t.strand, mt, cds)
            for key in sorted(uORF_dict.keys()):
                #print(key,len(uORF_dict[key]))
                for it in uORF_dict[key]:
                    #print(it)
                    uORF_seq.loc[index] = it
                    index += 1
            #if index > 100:
            #    break
        uORF_seq.to_csv(args.output, sep=',', index=False)
    else:
        for t in db.features_of_type(mRNA_str, order_by='start'):
            # primary transcript (pt) 是基因组上的转录本的序列，
            # 有的会包括intron，所以提取的序列和matural transcript 不一致
            # print(t)
            if args.transcript in t.id:
                pt = t.sequence(args.genome, use_strand=True)
                # matural transcript (mt)
                # exon 提取的是转录本内成熟的MRNA的序列,即外显子收尾相连的matural transcript
                mt = ''
                for e in db.children(t, featuretype='exon', order_by='start'):
                    s = e.sequence(args.genome, use_strand=False) # 不反向互补，对于负链要得到全部的cds后再一次性反向互补
                    mt += s
                mt = Seq(mt)
                if t.strand == '-':
                    mt = mt.reverse_complement()
                # CDS 提取的是编码区 ATG ... TAG
                cds = ''
                for c in db.children(t, featuretype='CDS', order_by='start'):
                    #print(c)
                    s = c.sequence(args.genome, use_strand=False) # 不反向互补，对于负链要得到全部的cds后再一次性反向互补
                    cds += s
                if args.style == 'GTF':
                    sc_seq = stop_codon_seq(db, t, args.genome)
                    cds = add_stop_codon(cds, t.strand, sc_seq)
                cds = Seq(cds)
                if t.strand == '-':
                    cds = cds.reverse_complement()
                uORF_dict = uorf(t.id, t.chrom, t.strand, mt, cds)
                for key in sorted(uORF_dict.keys()):
                    #print(key,len(uORF_dict[key]))
                    for it in uORF_dict[key]:
                        #print(it)
                        uORF_seq.loc[index] = it
                        index += 1
                uORF_seq.to_csv(args.output, sep=',', index=False)
                break 
