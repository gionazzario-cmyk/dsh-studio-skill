import Foundation
import Vision
import AppKit
let args = CommandLine.arguments
guard args.count > 1, let img = NSImage(contentsOfFile: args[1]),
      let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
    fputs("ERR image\n", stderr); exit(2)
}
let req = VNRecognizeTextRequest()
req.recognitionLevel = .accurate
req.usesLanguageCorrection = true
req.recognitionLanguages = ["it-IT", "en-US"]
try VNImageRequestHandler(cgImage: cg).perform([req])
for obs in req.results ?? [] {
    if let c = obs.topCandidates(1).first { print(c.string) }
}
