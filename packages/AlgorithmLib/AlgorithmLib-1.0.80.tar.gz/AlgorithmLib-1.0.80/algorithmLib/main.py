from operator import methodcaller
from computeAudioQuality.mainProcess import computeAudioQuality
from ctypes import  *


def compute_audio_quality(metrics, testFile=None, refFile=None, cleFile=None, outFile=None, noiseFile=None,
                              samplerate=16000, bitwidth=2, channel=1, refOffset=0, testOffset=0, maxComNLevel=-48.0,
                              speechPauseLevel=-35.0):
    """
    :param metrics: G160/P563/POLQA/PESQ/STOI/STI/PEAQ/SDR/SII/LOUDNESS/MUSIC/MATCH/TRANSIENT，必选项
    # G160 无采样率限制；  WAV/PCM输入 ；三端输入: clean、ref、test；无时间长度要求；
    # P563 8000hz(其他采样率会强制转换到8khz)；  WAV/PCM输入 ；单端输入: test；时长 < 20s；
    # POLQA 窄带模式  8k  超宽带模式 48k ；WAV/PCM输入 ；双端输入：ref、test；时长 < 20s；
    # PESQ 窄带模式  8k   宽带模式 16k ；WAV/PCM输入 ；双端输入：ref、test；时长 < 20s；
    # STOI 无采样率限制; 双端输入：ref、test；无时间长度要求；
    # STI >8k(实际会计算8khz的频谱)； WAV/PCM输入 ；双端输入：ref、test；时长 > 20s
    # PEAQ 无采样率限制；WAV/PCM输入 ；双端输入：ref、test；无时间长度要求；
    # SDR 无采样率限制; WAV/PCM输入 ; 双端输入：ref、test；无时间长度要求；
    # MATCH 无采样率限制; WAV/PCM输入;三端输入：ref、test、out； 无时间长度要求；
    # MUSIC 无采样率限制;WAV/PCM输入;双端输入：ref、test；无时间长度要求；
    #
    不同指标输入有不同的采样率要求，如果传入的文件不符合该指标的要求，会自动变采样到合法的区间
    :param testFile: 被测文件，必选项
    :param refFile:  参考文件，可选项，全参考指标必选，比如POLQA/PESQ/PEAQ
    :param cleFile:  干净语音文件，可选项，G160,TRANSIENT需要
    :param noiseFile 噪声文件，可选项，突发噪声信噪比计算需要
    :param outFile 输出文件，可选项，对其文件可选
    :param samplerate: 采样率，可选项，pcm文件需要 default = 16000
    :param bitwidth: 比特位宽度，可选项，pcm文件需要 default = 2
    :param channel: 通道数，可选项，pcm文件需要 default = 1
    :param refOffset: ref文件的样点偏移，可选项，指标G160需要
    :param testOffset: test文件的样点偏移，可选项，指标G160需要
    :return:
    """
    paraDicts = {
        'metrics':metrics,
        'testFile':testFile,
        'refFile':refFile,
        'cleFile':cleFile,
        'noiseFile':noiseFile,
        'outFile':outFile,
        'samplerate':samplerate,
        'bitwidth':bitwidth,
        'channel':channel,
        'refOffset':refOffset,
        'testOffset':testOffset,
        'maxComNLevel':maxComNLevel,
        "speechPauseLevel":speechPauseLevel
    }
    comAuQUA = computeAudioQuality(**paraDicts)
    return methodcaller(metrics)(comAuQUA)

if __name__ == '__main__':

    speech = r'D:\AutoWork\audiotestalgorithm\algorithmLib\SNR_ESTIMATION\speech.wav'
    music = r'D:\AutoWork\audiotestalgorithm\algorithmLib\SNR_ESTIMATION\music_rap.wav'
    transi = r'D:\AutoWork\audiotestalgorithm\algorithmLib\SNR_ESTIMATION\transientNoise.wav'
    test = r'D:\AutoWork\audiotestalgorithm\algorithmLib\SNR_ESTIMATION\test.wav'
    res = compute_audio_quality('MUSIC',refFile=speech,testFile=music)

    print(res)

    res = compute_audio_quality('TRANSIENT',cleFile=speech,noiseFile=transi,testFile=test)
    print(res)

    res = compute_audio_quality('MATCH',refFile=speech,testFile=test,outFile='123.wav')
    print(res)
    #print(compute_audio_quality('G160', testFile=src,refFile=src,samplerate=16000))

    #print(match_sig(refFile='speech.wav', targetFile='test.wav', outFile='outfile.wav'))
    pass