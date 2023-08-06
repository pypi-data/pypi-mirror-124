import unittest
import os
import sbol2

from sequences_to_features import FeatureLibrary
from sequences_to_features import FeatureAnnotater
from sequences_to_features import FeaturePruner
from features_to_circuits import CircuitLibrary
from features_to_circuits import CircuitBuilder

class CurationTests(unittest.TestCase):

    # Remove all overlapping features from copy of target construct
    # Do not remove copy of target construct since it is not identical to original
    def test_pruning_overlapping(self):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

        HOMESPACE = 'http://synbict.org'

        MIN_TARGET_LENGTH = 800

        sbol2.setHomespace(HOMESPACE)
        sbol2.Config.setOption('validate', False)
        sbol2.Config.setOption('sbol_typed_uris', False)

        cello_doc = load_sbol(os.path.join(__location__, 'cello_library.xml'))
        feature_library = FeatureLibrary([cello_doc])

        target_doc = load_sbol(os.path.join(__location__, 'simple_device.xml'))
        target_construct_library = FeatureLibrary([target_doc], True)

        dummy_canonical_library = FeatureLibrary([], False)

        feature_annotater = FeatureAnnotater(feature_library, 40)
        annotated_identities = feature_annotater.annotate(target_construct_library, MIN_TARGET_LENGTH)

        added_features = target_construct_library.update()

        feature_pruner = FeaturePruner(feature_library)
        feature_pruner.prune(target_construct_library, 14, MIN_TARGET_LENGTH, False, dummy_canonical_library, keep_flat=False)

        annotated_features = []
        annotating_features = []

        for added_feature in added_features:
            if added_feature.identity in annotated_identities:
                annotated_features.append(added_feature)
            else:
                annotating_features.append(added_feature)

        feature_pruner.clean(target_construct_library, annotated_features, annotating_features)

        pruned_definition = target_doc.getComponentDefinition('/'.join([HOMESPACE, 'UnnamedPart', '1']))

        self.assertEqual(len(target_doc.componentDefinitions), 2,
            "Cleaned document does not contain exactly two ComponentDefinitions. Should contain two for UnnamedPart and none for pBAD or L3S3P11.")
        self.assertEqual(len(target_doc.sequences), 1,
            "Cleaned document does not contain exactly one Sequence. Should contain one for UnnamedPart and none for pBAD or L3S3P11.")
        self.assertEqual(len(pruned_definition.sequenceAnnotations), 1,
            "Pruned ComponentDefinition does not contain exactly one SequenceAnnotation. Should contain one for CDS and none for pBAD, L3S3P11, promoter, or terminator.")
        self.assertEqual(len(pruned_definition.components), 0,
            "Pruned ComponentDefinition does not contain exactly zero Components. Should contain none for pBAD or L3S3P11.")

    # Remove promoter and terminator features from copy of target construct
    # Then remove copy of target construct since it is identical to original
    # Also remove promoter and terminator since they are no longer sub-parts of any construct
    def test_pruning_annotated(self):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

        HOMESPACE = 'http://synbict.org'

        MIN_TARGET_LENGTH = 800

        sbol2.setHomespace(HOMESPACE)
        sbol2.Config.setOption('validate', False)
        sbol2.Config.setOption('sbol_typed_uris', False)

        cello_doc = load_sbol(os.path.join(__location__, 'cello_library.xml'))
        feature_library = FeatureLibrary([cello_doc])

        target_doc = load_sbol(os.path.join(__location__, 'simple_device.xml'))
        target_construct_library = FeatureLibrary([target_doc], True)

        dummy_canonical_library = FeatureLibrary([], False)

        feature_annotater = FeatureAnnotater(feature_library, 40)
        annotated_identities = feature_annotater.annotate(target_construct_library, MIN_TARGET_LENGTH)

        added_features = target_construct_library.update()

        feature_pruner = FeaturePruner(feature_library)
        feature_pruner.prune(target_construct_library, 14, MIN_TARGET_LENGTH, False, dummy_canonical_library)

        annotated_features = []
        annotating_features = []

        for added_feature in added_features:
            if added_feature.identity in annotated_identities:
                annotated_features.append(added_feature)
            else:
                annotating_features.append(added_feature)

        feature_pruner.clean(target_construct_library, annotated_features, annotating_features)

        self.assertEqual(len(target_doc.componentDefinitions), 1,
            "Cleaned document does not contain exactly one ComponentDefinition. Should contain one for UnnamedPart and none for pBAD or L3S3P11.")
        self.assertEqual(len(target_doc.sequences), 1,
            "Cleaned document does not contain exactly one Sequence. Should contain one for UnnamedPart and none for pBAD or L3S3P11.")

    def test_curate_nand_circuit(self):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

        HOMESPACE = 'http://synbict.org'
        VERSION = '1'

        MIN_TARGET_LENGTH = 2000

        sbol2.setHomespace(HOMESPACE)
        sbol2.Config.setOption('validate', False)
        sbol2.Config.setOption('sbol_typed_uris', False)

        cello_doc = load_sbol(os.path.join(__location__, 'cello_library.xml'))
        feature_library = FeatureLibrary([cello_doc])

        target_doc = load_sbol(os.path.join(__location__, 'genetic_nand.xml'))
        target_construct_library = FeatureLibrary([target_doc], True)

        feature_annotater = FeatureAnnotater(feature_library, 40)
        feature_annotater.annotate(target_construct_library, MIN_TARGET_LENGTH)

        feature_pruner = FeaturePruner(feature_library)
        feature_pruner.prune(target_construct_library, 14, MIN_TARGET_LENGTH, False, feature_library, True, False)

        circuit_library = CircuitLibrary([cello_doc])
        target_device_library = FeatureLibrary([target_doc], require_sequence=False)

        circuit_ID = 'nand_circuit'

        circuit_builder = CircuitBuilder(circuit_library)
        circuit_builder.build(circuit_ID, target_doc,
            target_device_library.get_features(MIN_TARGET_LENGTH, True), VERSION)

        nand_circuit = target_doc.getModuleDefinition('/'.join([HOMESPACE, circuit_ID]))

        nand_devices = {
            '/'.join([HOMESPACE, 'Strain_4_MG1655_Genomic_NAND_Circuit', VERSION])
        }

        devices = set()

        for device in nand_circuit.functionalComponents:
            devices.add(device.definition)

        device_intersection = nand_devices.intersection(devices)
        device_difference = nand_devices.difference(devices)

        nand_sub_circuits = {
            'https://synbiohub.programmingbiology.org/public/Cello_Parts/YFP_protein_production/1',
            'https://synbiohub.programmingbiology.org/public/Cello_Parts/PhlF_pPhlF_repression/1',
            'https://synbiohub.programmingbiology.org/public/Cello_Parts/IcaRA_protein_production/1',
            'https://synbiohub.programmingbiology.org/public/Cello_Parts/PhlF_protein_production/1',
            'https://synbiohub.programmingbiology.org/public/Cello_Parts/LacI_pTac_repression/1',
            'https://synbiohub.programmingbiology.org/public/Cello_Parts/TetR_protein_production/1',
            'https://synbiohub.programmingbiology.org/public/Cello_Parts/IcaRA_pIcaRA_repression/1',
            'https://synbiohub.programmingbiology.org/public/Cello_Parts/LacI_protein_production/1'
        }

        sub_circuits = set()

        for sub_circuit in nand_circuit.modules:
            sub_circuits.add(sub_circuit.definition)

        sub_circuit_intersection = nand_sub_circuits.intersection(sub_circuits)
        sub_circuit_difference = nand_sub_circuits.difference(sub_circuits)

        self.assertEqual(len(device_intersection), len(nand_devices),
            "Inferred circuit is missing expected devices: {mi}".format(mi=', '.join(device_difference)))
        self.assertEqual(len(sub_circuit_intersection), len(nand_sub_circuits),
            "Inferred circuit is missing expected sub-circuits: {mi}".format(mi=', '.join(sub_circuit_difference)))

if __name__ == '__main__':
    unittest.main()
