#!/bin/python
import sys

defaults = {
    'PR': {'H': 'High (H)', 'L': 'Low (L)', 'N': 'None (N)'},
    'A': {'H': 'High (H)', 'L': 'Low (L)', 'N': 'None (N)'},
    'C': {'H': 'High (H)', 'L': 'Low (L)', 'N': 'None (N)'},
    'I': {'H': 'High (H)', 'L': 'Low (L)', 'N': 'None (N)'},
    'AC': {'H': 'High (H)', 'L': 'Low (L)'},
    'S': {'C': 'Changed (C)', 'U': 'Unchanged (U)'},
    'UI': {'R': 'Required (R)', 'N': 'None (N)'},
    'AV': {'A': 'Adjacent (A)', 'P': 'Physical (P)',
           'L': 'Local (L)', 'N': 'Network (N)'}
}

area_names = {
    "AV": "Attack Vector",
    "AC": "Attack Complexity",
    "PR": "Privileges Required",
    "UI": "User Interaction",
    "S": "Scope",
    "C": "Confidentiality",
    "I": "Integrity",
    "A": "Availability",
}

labels = {
    "AV_N_Label": "A vulnerability exploitable with network access means the vulnerable component is bound to the network stack and the attacker's path is through OSI layer 3 (the network layer). Such a vulnerability is often termed \"remotely exploitable\" and can be thought of as an attack being exploitable one or more network hops away.",
    "AV_A_Label": "A vulnerability exploitable with adjacent network access means the vulnerable component is bound to the network stack, however the attack is limited to the same shared physical (e.g. Bluetooth, IEEE 802.11), or logical (e.g. local IP subnet) network, and cannot be performed across an OSI layer 3 boundary (e.g. a router).",
    "AV_L_Label": "A vulnerability exploitable with local access means that the vulnerable component is not bound to the network stack, and the attacker's path is via read/write/execute capabilities. In some cases, the attacker may be logged in locally in order to exploit the vulnerability, otherwise, she may rely on User Interaction to execute a malicious file.",
    "AV_P_Label": "A vulnerability exploitable with physical access requires the attacker to physically touch or manipulate the vulnerable component. Physical interaction may be brief or persistent.",
    "AC_L_Label": "Specialized access conditions or extenuating circumstances do not exist. An attacker can expect repeatable success against the vulnerable component.",
    "AC_H_Label": "A successful attack depends on conditions beyond the attacker's control. That is, a successful attack cannot be accomplished at will, but requires the attacker to invest in some measurable amount of effort in preparation or execution against the vulnerable component before a successful attack can be expected. For example, a successful attack may require the attacker: to perform target-specific reconnaissance; to prepare the target environment to improve exploit reliability; or to inject herself into the logical network path between the target and the resource requested by the victim in order to read and/or modify network communications (e.g. a man in the middle attack).",
    "PR_N_Label": "The attacker is unauthorized prior to attack, and therefore does not require any access to settings or files to carry out an attack.",
    "PR_L_Label": "The attacker is authorized with (i.e. requires) privileges that provide basic user capabilities that could normally affect only settings and files owned by a user. Alternatively, an attacker with Low privileges may have the ability to cause an impact only to non-sensitive resources.",
    "PR_H_Label": "The attacker is authorized with (i.e. requires) privileges that provide significant (e.g. administrative) control over the vulnerable component that could affect component-wide settings and files.",
    "UI_N_Label": "The vulnerable system can be exploited without any interaction from any user.",
    "UI_R_Label": "Successful exploitation of this vulnerability requires a user to take some action before the vulnerability can be exploited.",
    "S_U_Label": "An exploited vulnerability can only affect resources managed by the same authority. In this case the vulnerable component and the impacted component are the same.",
    "S_C_Label": "An exploited vulnerability can affect resources beyond the authorization privileges intended by the vulnerable component. In this case the vulnerable component and the impacted component are different.",
    "C_N_Label": "There is no loss of confidentiality within the impacted component.",
    "C_L_Label": "There is some loss of confidentiality. Access to some restricted information is obtained, but the attacker does not have control over what information is obtained, or the amount or kind of loss is constrained. The information disclosure does not cause a direct, serious loss to the impacted component.",
    "C_H_Label": "There is total loss of confidentiality, resulting in all resources within the impacted component being divulged to the attacker. Alternatively, access to only some restricted information is obtained, but the disclosed information presents a direct, serious impact.",
    "I_N_Label": "There is no loss of integrity within the impacted component.",
    "I_L_Label": "Modification of data is possible, but the attacker does not have control over the consequence of a modification, or the amount of modification is constrained. The data modification does not have a direct, serious impact on the impacted component.",
    "I_H_Label": "There is a total loss of integrity, or a complete loss of protection. For example, the attacker is able to modify any/all files protected by the impacted component. Alternatively, only some files can be modified, but malicious modification would present a direct, serious consequence to the impacted component.",
    "A_N_Label": "There is no impact to availability within the impacted component.",
    "A_L_Label": "There is reduced performance or interruptions in resource availability. Even if repeated exploitation of the vulnerability is possible, the attacker does not have the ability to completely deny service to legitimate users. The resources in the impacted component are either partially available all of the time, or fully available only some of the time, but overall there is no direct, serious consequence to the impacted component.",
    "A_H_Label": "There is total loss of availability, resulting in the attacker being able to fully deny access to resources in the impacted component; this loss is either sustained (while the attacker continues to deliver the attack) or persistent (the condition persists even after the attack has completed). Alternatively, the attacker has the ability to deny some availability, but the loss of availability presents a direct, serious consequence to the impacted component (e.g., the attacker cannot disrupt existing connections, but can prevent new connections; the attacker can repeatedly exploit a vulnerability that, in each instance of a successful attack, leaks a only small amount of memory, but after repeated exploitation causes a service to become completely unavailable).",
    "E_X_Label": "Assigning this value to the metric will not influence the score.",
    "E_U_Label": "No exploit code is available, or an exploit is theoretical.",
    "E_P_Label": "Proof-of-concept exploit code is available, or an attack demonstration is not practical for most systems. The code or technique is not functional in all situations and may require substantial modification by a skilled attacker.",
    "E_F_Label": "Functional exploit code is available. The code works in most situations where the vulnerability exists.",
    "E_H_Label": "Functional autonomous code exists, or no exploit is required (manual trigger) and details are widely available. Exploit code works in every situation, or is actively being delivered via an autonomous agent (such as a worm or virus). Network-connected systems are likely to encounter scanning or exploitation attempts. Exploit development has reached the level of reliable, widely-available, easy-to-use automated tools.",
    "RL_X_Label": "Assigning this value to the metric will not influence the score.",
    "RL_O_Label": "A complete vendor solution is available. Either the vendor has issued an official patch, or an upgrade is available.",
    "RL_T_Label": "There is an official but temporary fix available. This includes instances where the vendor issues a temporary hotfix, tool, or workaround.",
    "RL_W_Label": "There is an unofficial, non-vendor solution available. In some cases, users of the affected technology will create a patch of their own or provide steps to work around or otherwise mitigate the vulnerability.",
    "RL_U_Label": "There is either no solution available or it is impossible to apply.",
    "RC_X_Label": "Assigning this value to the metric will not influence the score.",
    "RC_U_Label": "There are reports of impacts that indicate a vulnerability is present. The reports indicate that the cause of the vulnerability is unknown, or reports may differ on the cause or impacts of the vulnerability. Reporters are uncertain of the true nature of the vulnerability, and there is little confidence in the validity of the reports or whether a static Base score can be applied given the differences described. An example is a bug report which notes that an intermittent but non-reproducible crash occurs, with evidence of memory corruption suggesting that denial of service, or possible more serious impacts, may result.",
    "RC_R_Label": "Significant details are published, but researchers either do not have full confidence in the root cause, or do not have access to source code to fully confirm all of the interactions that may lead to the result. Reasonable confidence exists, however, that the bug is reproducible and at least one impact is able to be verified (Proof-of-concept exploits may provide this). An example is a detailed write-up of research into a vulnerability with an explanation (possibly obfuscated or 'left as an exercise to the reader') that gives assurances on how to reproduce the results.",
    "RC_C_Label": "Detailed reports exist, or functional reproduction is possible (functional exploits may provide this). Source code is available to independently verify the assertions of the research, or the author or vendor of the affected code has confirmed the presence of the vulnerability.",
    "CR_X_Label": "Assigning this value to the metric will not influence the score.",
    "CR_L_Label": "Loss of Confidentiality is likely to have only a limited adverse effect on the organization or individuals associated with the organization (e.g., employees, customers).",
    "CR_M_Label": "Assigning this value to the metric will not influence the score.",
    "CR_H_Label": "Loss of Confidentiality is likely to have a catastrophic adverse effect on the organization or individuals associated with the organization (e.g., employees, customers).",
    "IR_X_Label": "Assigning this value to the metric will not influence the score.",
    "IR_L_Label": "Loss of Integrity is likely to have only a limited adverse effect on the organization or individuals associated with the organization (e.g., employees, customers).",
    "IR_M_Label": "Assigning this value to the metric will not influence the score.",
    "IR_H_Label": "Loss of Integrity is likely to have a catastrophic adverse effect on the organization or individuals associated with the organization (e.g., employees, customers).",
    "AR_X_Label": "Assigning this value to the metric will not influence the score.",
    "AR_L_Label": "Loss of Availability is likely to have only a limited adverse effect on the organization or individuals associated with the organization (e.g., employees, customers).",
    "AR_M_Label": "Assigning this value to the metric will not influence the score.",
    "AR_H_Label": "Loss of Availability is likely to have a catastrophic adverse effect on the organization or individuals associated with the organization (e.g., employees, customers).",
    "MAV_X_Label": "Use the value assigned to the corresponding Base Score metric.",
    "MAV_N_Label": "A vulnerability exploitable with network access means the vulnerable component is bound to the network stack and the attacker's path is through OSI layer 3 (the network layer). Such a vulnerability is often termed \"remotely exploitable\" and can be thought of as an attack being exploitable one or more network hops away.",
    "MAV_A_Label": "A vulnerability exploitable with adjacent network access means the vulnerable component is bound to the network stack, however the attack is limited to the same shared physical (e.g. Bluetooth, IEEE 802.11), or logical (e.g. local IP subnet) network, and cannot be performed across an OSI layer 3 boundary (e.g. a router).",
    "MAV_L_Label": "A vulnerability exploitable with local access means that the vulnerable component is not bound to the network stack, and the attacker's path is via read/write/execute capabilities. In some cases, the attacker may be logged in locally in order to exploit the vulnerability, otherwise, she may rely on User Interaction to execute a malicious file.",
    "MAV_P_Label": "A vulnerability exploitable with physical access requires the attacker to physically touch or manipulate the vulnerable component. Physical interaction may be brief or persistent.",
    "MAC_X_Label": "Use the value assigned to the corresponding Base Score metric.",
    "MAC_L_Label": "Specialized access conditions or extenuating circumstances do not exist. An attacker can expect repeatable success against the vulnerable component.",
    "MAC_H_Label": "A successful attack depends on conditions beyond the attacker's control. That is, a successful attack cannot be accomplished at will, but requires the attacker to invest in some measurable amount of effort in preparation or execution against the vulnerable component before a successful attack can be expected. For example, a successful attack may require the attacker: to perform target-specific reconnaissance; to prepare the target environment to improve exploit reliability; or to inject herself into the logical network path between the target and the resource requested by the victim in order to read and/or modify network communications (e.g. a man in the middle attack).",
    "MPR_X_Label": "Use the value assigned to the corresponding Base Score metric.",
    "MPR_N_Label": "The attacker is unauthorized prior to attack, and therefore does not require any access to settings or files to carry out an attack.",
    "MPR_L_Label": "The attacker is authorized with (i.e. requires) privileges that provide basic user capabilities that could normally affect only settings and files owned by a user. Alternatively, an attacker with Low privileges may have the ability to cause an impact only to non-sensitive resources.",
    "MPR_H_Label": "The attacker is authorized with (i.e. requires) privileges that provide significant (e.g. administrative) control over the vulnerable component that could affect component-wide settings and files.",
    "MUI_X_Label": "Use the value assigned to the corresponding Base Score metric.",
    "MUI_N_Label": "The vulnerable system can be exploited without any interaction from any user.",
    "MUI_R_Label": "Successful exploitation of this vulnerability requires a user to take some action before the vulnerability can be exploited.",
    "MS_X_Label": "Use the value assigned to the corresponding Base Score metric.",
    "MS_U_Label": "An exploited vulnerability can only affect resources managed by the same authority. In this case the vulnerable component and the impacted component are the same.",
    "MS_C_Label": "An exploited vulnerability can affect resources beyond the authorization privileges intended by the vulnerable component. In this case the vulnerable component and the impacted component are different.",
    "MC_X_Label": "Use the value assigned to the corresponding Base Score metric.",
    "MC_N_Label": "There is no loss of confidentiality within the impacted component.",
    "MC_L_Label": "There is some loss of confidentiality. Access to some restricted information is obtained, but the attacker does not have control over what information is obtained, or the amount or kind of loss is constrained. The information disclosure does not cause a direct, serious loss to the impacted component.",
    "MC_H_Label": "There is total loss of confidentiality, resulting in all resources within the impacted component being divulged to the attacker. Alternatively, access to only some restricted information is obtained, but the disclosed information presents a direct, serious impact.",
    "MI_X_Label": "Use the value assigned to the corresponding Base Score metric.",
    "MI_N_Label": "There is no loss of integrity within the impacted component.",
    "MI_L_Label": "Modification of data is possible, but the attacker does not have control over the consequence of a modification, or the amount of modification is constrained. The data modification does not have a direct, serious impact on the impacted component.",
    "MI_H_Label": "There is a total loss of integrity, or a complete loss of protection. For example, the attacker is able to modify any/all files protected by the impacted component. Alternatively, only some files can be modified, but malicious modification would present a direct, serious consequence to the impacted component.",
    "MA_X_Label": "Use the value assigned to the corresponding Base Score metric.",
    "MA_N_Label": "There is no impact to availability within the impacted component.",
    "MA_L_Label": "There is reduced performance or interruptions in resource availability. Even if repeated exploitation of the vulnerability is possible, the attacker does not have the ability to completely deny service to legitimate users. The resources in the impacted component are either partially available all of the time, or fully available only some of the time, but overall there is no direct, serious consequence to the impacted component.",
    "MA_H_Label": "There is total loss of availability, resulting in the attacker being able to fully deny access to resources in the impacted component; this loss is either sustained (while the attacker continues to deliver the attack) or persistent (the condition persists even after the attack has completed). Alternatively, the attacker has the ability to deny some availability, but the loss of availability presents a direct, serious consequence to the impacted component (e.g., the attacker cannot disrupt existing connections, but can prevent new connections; the attacker can repeatedly exploit a vulnerability that, in each instance of a successful attack, leaks a only small amount of memory, but after repeated exploitation causes a service to become completely unavailable)."
}


if len(sys.argv) != 2:
    print("usage: cvss2markdown.py <cvss vector>")
    sys.exit(1)

vec = sys.argv[1]

components = vec.split("/")

if components[0].startswith("CVSS"):
    # slice off the starting "CVSS" portion
    # if included
    components = components[1:]

mid, bot = "| ", "| "
iheader = "| "
paras = ""

for component in components:
    area, value = component.split(":")

    if area not in defaults:
        print("This tool _only_ handles base score calculation.")
        sys.exit(2)

    if value not in defaults[area]:
        print("Invalid value provided as CVSS attribute value.")
        sys.exit(3)

    label = "{0}_{1}_Label".format(area, value)

    lval = labels[label]

    paras += "{0}\n\n".format(lval)

    iheader += "{0} | ".format(area)
    mid += ":---: | "
    bot += "{0} | ".format(defaults[area][value])

print(iheader)
print(mid)
print(bot)
print("\n", paras)
